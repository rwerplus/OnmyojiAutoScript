# This Python file uses the following encoding: utf-8
"""
Lightweight context for tools_gui.py.

Quacks like ``module.gui.context.process_manager.ProcessManager`` for the subset
of slots that the QML "Tools" panel and the MirrorImage component actually use,
but **does not** spawn a per-config ``ScriptProcess`` over zerorpc. Everything
runs in-process against a single ``Device`` instance, which is what makes the
Tools-only launcher fast.

Two modes:

- **Live mode** (default): a single ``Device`` is initialized lazily on first
  screenshot. ``click`` / ``swipe`` / ``test_ocr`` go through ADB.
- **Static-image mode** (``image_path`` set): no Device ever spins up;
  ``gui_mirror_image`` returns a cached QImage of the supplied screenshot,
  ``test_ocr`` / ``test_image_match`` run against the cached numpy array,
  ``click`` / ``swipe`` are warning-logged no-ops. Useful for editing rules
  offline against an existing screenshot.

QML side touchpoints (do not break these):

- ``process_manager.gui_menu()``                          -> tree menu JSON
- ``process_manager.add(configName)``                     -> no-op
- ``process_manager.gui_mirror_image(scriptName)``        -> QImage (live or cached)
- ``process_manager.gui_args / gui_task / gui_set_task*`` -> stubs (Tools panel
  never reaches the Args.qml branch in our window, but the methods exist so
  any stray QML binding does not raise AttributeError)
- ``process_manager.default_tool()``                      -> Chinese tool name
- ``process_manager.is_static_mode()``                    -> bool

Plus convenience slots so the tool editors can actually exercise the device
(or the static image, in static mode):

- ``click(x, y)``, ``long_click(x, y, duration_ms)``
- ``swipe(x1, y1, x2, y2, duration_ms)``
- ``test_image_match(roi_front, roi_back, threshold, file_path)`` -> hit JSON
- ``test_ocr(roi, mode)``                                -> recognized text
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QImage

from module.logger import logger


# Tools menu — Chinese labels matching ToolsWindow.qml. Kept as a module-level
# constant so we do not import ConfigMenu (which would pull in the whole
# pydantic ConfigModel just to read this list). The mapping label -> qml file
# lives in ToolsWindow.qml::loadTool(); keep both lists in sync.
TOOLS_MENU = [
    '图像规则',
    '文字识别',
    '点击规则',
    '长按规则',
    '滑动规则',
    '列表规则',
]


def _pick_default_config_name() -> str:
    """
    Pick the first non-template config under ``config/*.json`` for Device init.

    The Tools panel does not actually read game-specific config (it only needs
    ADB/screenshot wiring), but Device requires *some* Config. We prefer an
    existing user config so the user does not have to set serial/screenshot
    method again.
    """
    config_dir = Path.cwd() / 'config'
    if not config_dir.exists():
        return 'oas'
    for p in sorted(config_dir.glob('*.json')):
        if p.stem == 'template':
            continue
        return p.stem
    return 'oas'


class LiteContext(QObject):
    """
    In-process replacement for ProcessManager, scoped to the Tools panel.
    """

    # Signals kept for API parity with ProcessManager. They are never emitted
    # in tools_gui.py, but exist so QML ``process_manager.xxx.connect(...)``
    # bindings never blow up if the panel ever pulls in Overview-style code.
    log_signal = Signal(str, str)
    sig_update_task = Signal(str, str)
    sig_update_pending = Signal(str, str)
    sig_update_waiting = Signal(str, str)

    def __init__(self,
                 config_name: Optional[str] = None,
                 image_path: Optional[str] = None,
                 default_tool: Optional[str] = None) -> None:
        """
        Args:
            config_name: name under config/ (without .json) bound to Device.
                Ignored when ``image_path`` is provided (no Device init).
            image_path: optional path to a screenshot. When set, LiteContext
                runs in **static mode**: ``gui_mirror_image`` returns the
                cached image, ``test_ocr`` / ``test_image_match`` run against
                that same image, and ``click`` / ``swipe`` are no-ops with a
                warning. Device is never initialized — useful for editing
                rules offline against an existing screenshot.
            default_tool: which tool tab the QML window should land on
                initially (Chinese label, e.g. '图像规则'). QML reads this
                via the ``default_tool()`` slot.
        """
        super().__init__()
        self._config_name = config_name or _pick_default_config_name()
        self._config = None
        self._device = None
        self._device_lock = threading.Lock()
        self._default_tool = default_tool or ''

        # --- Static image cache -------------------------------------------
        # In static mode we hold both a QImage (for QML's mirror viewer) and
        # an RGB numpy array (so RuleOcr/RuleImage see the same format
        # device.screenshot() would have returned — RGB, uint8, HxWx3).
        self._static_mode = False
        self._static_image_path: Optional[str] = None
        self._static_image_qt: Optional[QImage] = None
        self._static_image_rgb: Optional[np.ndarray] = None
        if image_path:
            self._load_static_image(image_path)

        if self._static_mode:
            logger.info(f'LiteContext: static mode, image="{self._static_image_path}"')
        else:
            logger.info(f'LiteContext bound to config "{self._config_name}"')

    # ------------------------------------------------------------------
    # Static image loading
    # ------------------------------------------------------------------

    def _load_static_image(self, path: str) -> None:
        """Load ``path`` into both a QImage and an RGB numpy array.

        Uses ``np.fromfile`` + ``cv2.imdecode`` to be safe with non-ASCII
        paths on Windows (cv2.imread mishandles them). Falls back to a
        minimal warning + non-static mode on failure rather than crashing
        the launcher.
        """
        try:
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                logger.error(f'Static image not found: {abs_path}')
                return
            buf = np.fromfile(abs_path, dtype=np.uint8)
            bgr = cv2.imdecode(buf, cv2.IMREAD_COLOR)
            if bgr is None:
                logger.error(f'cv2 failed to decode {abs_path}')
                return
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            h, w, _ = rgb.shape
            qimg = QImage(rgb.tobytes(), w, h, w * 3, QImage.Format_RGB888).copy()
        except Exception:
            logger.exception(f'Failed to load static image {path!r}')
            return

        self._static_mode = True
        self._static_image_path = abs_path
        self._static_image_rgb = rgb
        self._static_image_qt = qimg

    # ------------------------------------------------------------------
    # Device / Config (lazy)
    # ------------------------------------------------------------------

    @property
    def static_mode(self) -> bool:
        return self._static_mode

    @property
    def config(self):
        if self._config is None:
            from module.config.config import Config
            self._config = Config(config_name=self._config_name)
        return self._config

    @property
    def device(self):
        if self._static_mode:
            # Caller is responsible for checking static_mode first. Raising
            # here makes accidental device use in static mode loud.
            raise RuntimeError('LiteContext is in static-image mode; '
                               'no Device is available')
        if self._device is None:
            with self._device_lock:
                if self._device is None:
                    from module.device.device import Device
                    logger.info('LiteContext: initializing Device (first use)')
                    self._device = Device(config=self.config)
        return self._device

    def warmup(self) -> None:
        """
        Force Device init up front. Call this from the entry script after the
        QML window appears so the very first screenshot tick does not stall
        the UI thread for a couple of seconds. No-op in static mode.
        """
        if self._static_mode:
            return
        try:
            _ = self.device
            self.device.screenshot()
        except Exception:
            logger.exception('LiteContext warmup failed; will retry on demand')

    # ------------------------------------------------------------------
    # ProcessManager-compatible slots used by QML
    # ------------------------------------------------------------------

    @Slot(result='QString')
    def gui_menu(self) -> str:
        """Return a Tools-only menu so ScriptView/ToolsWindow only shows tools."""
        return json.dumps({'Tools': TOOLS_MENU}, ensure_ascii=False)

    @Slot(str)
    def add(self, _config: str) -> None:
        """No ScriptProcess spawn — Device is created lazily on first use."""
        return None

    @Slot(str, result='QImage')
    def gui_mirror_image(self, _config: str) -> QImage:
        """
        Provide a screenshot to MirrorImage.qml.

        - Static mode: return the cached QImage every tick. The QML Timer
          keeps polling at 1Hz but each call is essentially a memcpy, so the
          ROI editor stays responsive without ever talking to ADB.
        - Live mode: capture via ``Device`` and convert to QImage.
        """
        if self._static_mode:
            if self._static_image_qt is None:
                return QImage()
            # Hand QML a copy so it cannot accidentally mutate our cache.
            return QImage(self._static_image_qt)

        try:
            frame = self.device.screenshot()
        except Exception:
            logger.exception('LiteContext.gui_mirror_image: screenshot failed')
            return QImage()

        # Device.screenshot() returns RGB by convention; QImage Format_RGB888
        # expects RGB. Copy so the QImage owns its buffer (the numpy array
        # gets reused by the next screenshot).
        if frame is None:
            return QImage()
        if frame.dtype != np.uint8:
            frame = frame.astype(np.uint8)
        if frame.ndim != 3 or frame.shape[2] != 3:
            logger.warning(f'Unexpected screenshot shape {frame.shape}')
            return QImage()

        height, width, _ = frame.shape
        # numpy strides may include padding; pass bytesPerLine explicitly.
        bytes_per_line = width * 3
        qimg = QImage(
            frame.tobytes(), width, height, bytes_per_line, QImage.Format_RGB888,
        ).copy()
        # Keep stuck-record clean so the GUI screenshot timer does not trip
        # the click/screenshot stuck detectors built into Device.
        try:
            self.device.stuck_record_clear()
        except Exception:
            pass
        return qimg

    @Slot(result='QString')
    def default_tool(self) -> str:
        """Optional default tool tab (Chinese label). Empty if not set."""
        return self._default_tool

    @Slot(result=bool)
    def is_static_mode(self) -> bool:
        return self._static_mode

    @Slot(result='QString')
    def static_image_path(self) -> str:
        return self._static_image_path or ''

    # --- The methods below exist purely to satisfy QML bindings that the
    #     Tools panel never actually exercises. Returning empty strings/false
    #     is good enough; we do not want a stray Args.qml load to AttributeError.

    @Slot(str, str, result='QString')
    def gui_args(self, _config: str, _task: str) -> str:
        return ''

    @Slot(str, str, result='QString')
    def gui_task(self, _config: str, _task: str) -> str:
        return ''

    @Slot(str, str, str, str, str, result=bool)
    def gui_set_task(self, *_args, **_kwargs) -> bool:
        return False

    @Slot(str, str, str, str, bool, result=bool)
    def gui_set_task_bool(self, *_args, **_kwargs) -> bool:
        return False

    @Slot(str, str, str, str, float, result=bool)
    def gui_set_task_number(self, *_args, **_kwargs) -> bool:
        return False

    @Slot(str, result='QString')
    def gui_task_list(self, _config: str) -> str:
        return ''

    @Slot(str)
    def restart(self, _config: str) -> None:
        return None

    @Slot(str)
    def start_script(self, _config: str) -> None:
        return None

    @Slot(str)
    def stop_script(self, _config: str) -> None:
        return None

    # ------------------------------------------------------------------
    # New convenience slots — let QML rule editors actually exercise the
    # device via the test buttons we add to ToolsWindow's content panes.
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_roi(roi: str):
        try:
            x, y, w, h = (int(v) for v in roi.split(','))
            return x, y, w, h
        except Exception:
            logger.warning(f'Invalid ROI string: {roi!r}')
            return None

    @Slot(int, int)
    def click(self, x: int, y: int) -> None:
        if self._static_mode:
            logger.warning(f'click({x},{y}) ignored: static-image mode')
            return
        try:
            self.device.click(int(x), int(y), control_check=False, control_name='ToolsClick')
        except Exception:
            logger.exception('LiteContext.click failed')

    @Slot(int, int, int)
    def long_click(self, x: int, y: int, duration_ms: int) -> None:
        if self._static_mode:
            logger.warning(f'long_click({x},{y}) ignored: static-image mode')
            return
        try:
            seconds = max(0.05, float(duration_ms) / 1000.0)
            self.device.long_click(int(x), int(y), duration=(seconds, seconds + 0.1),
                                   control_name='ToolsLongClick')
        except Exception:
            logger.exception('LiteContext.long_click failed')

    @Slot(int, int, int, int, int)
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int) -> None:
        if self._static_mode:
            logger.warning(f'swipe({x1},{y1}->{x2},{y2}) ignored: static-image mode')
            return
        try:
            seconds = max(0.05, float(duration_ms) / 1000.0)
            self.device.swipe(p1=(int(x1), int(y1)), p2=(int(x2), int(y2)),
                              duration=(seconds, seconds + 0.05),
                              control_name='ToolsSwipe',
                              distance_check=False)
        except Exception:
            logger.exception('LiteContext.swipe failed')

    def _current_numpy_image(self) -> Optional[np.ndarray]:
        """Numpy RGB image for OCR / template matching. In static mode this
        is the cached image; otherwise a fresh device screenshot."""
        if self._static_mode:
            return self._static_image_rgb
        try:
            return self.device.screenshot()
        except Exception:
            logger.exception('screenshot failed for test slot')
            return None

    @Slot(str, str, result='QString')
    def test_ocr(self, roi: str, mode: str) -> str:
        """Run OCR over the given ROI. mode in
        {Full,Single,Digit,DigitCounter,Duration,Quantity}. Returns JSON.
        Uses the static image when in static mode."""
        from module.atom.ocr import RuleOcr
        bbox = self._parse_roi(roi)
        if bbox is None:
            return json.dumps({'ok': False, 'error': 'bad roi'})
        img = self._current_numpy_image()
        if img is None:
            return json.dumps({'ok': False, 'error': 'no image'})
        try:
            rule = RuleOcr(roi=bbox, area=bbox, mode=mode or 'Full',
                           method='Default', keyword='', name='tools_test')
            result = rule.ocr(img)
            return json.dumps({'ok': True, 'result': str(result)},
                              ensure_ascii=False)
        except Exception as e:
            logger.exception('LiteContext.test_ocr failed')
            return json.dumps({'ok': False, 'error': str(e)},
                              ensure_ascii=False)

    @Slot(str, str, float, str, result='QString')
    def test_image_match(self, roi_front: str, roi_back: str,
                         threshold: float, file_path: str) -> str:
        """Match the template at ``file_path`` (front ROI cropped from it)
        against the current image inside ``roi_back``. Uses the static image
        when in static mode. Returns JSON ``{ok, found}``."""
        from module.atom.image import RuleImage
        front = self._parse_roi(roi_front)
        back = self._parse_roi(roi_back)
        if front is None or back is None:
            return json.dumps({'ok': False, 'error': 'bad roi'})
        if not file_path or not os.path.exists(file_path):
            return json.dumps({'ok': False, 'error': 'file not found'})
        img = self._current_numpy_image()
        if img is None:
            return json.dumps({'ok': False, 'error': 'no image'})
        try:
            rule = RuleImage(roi_front=front, roi_back=back,
                             threshold=float(threshold or 0.8),
                             method='Template matching', file=file_path)
            found = bool(rule.match(img))
            return json.dumps({'ok': True, 'found': found})
        except Exception as e:
            logger.exception('LiteContext.test_image_match failed')
            return json.dumps({'ok': False, 'error': str(e)})
