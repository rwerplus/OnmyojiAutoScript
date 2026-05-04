# This Python file uses the following encoding: utf-8
"""
Lightweight context for tools_gui.py.

Quacks like ``module.gui.context.process_manager.ProcessManager`` for the subset
of slots that the QML "Tools" panel and the MirrorImage component actually use,
but **does not** spawn a per-config ``ScriptProcess`` over zerorpc. Everything
runs in-process against a single ``Device`` instance, which is what makes the
Tools-only launcher fast.

QML side touchpoints (do not break these):

- ``process_manager.gui_menu()``                          -> tree menu JSON
- ``process_manager.add(configName)``                     -> no-op
- ``process_manager.gui_mirror_image(scriptName)``        -> live screenshot QImage
- ``process_manager.gui_args / gui_task / gui_set_task*`` -> stubs (Tools panel
  never reaches the Args.qml branch in our window, but the methods exist so
  any stray QML binding does not raise AttributeError)

Plus convenience slots so the tool editors can actually exercise the device:

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

    def __init__(self, config_name: Optional[str] = None) -> None:
        super().__init__()
        self._config_name = config_name or _pick_default_config_name()
        self._config = None
        self._device = None
        self._device_lock = threading.Lock()
        logger.info(f'LiteContext bound to config "{self._config_name}"')

    # ------------------------------------------------------------------
    # Device / Config (lazy)
    # ------------------------------------------------------------------

    @property
    def config(self):
        if self._config is None:
            from module.config.config import Config
            self._config = Config(config_name=self._config_name)
        return self._config

    @property
    def device(self):
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
        the UI thread for a couple of seconds.
        """
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
        Capture a screenshot via ``Device`` and hand it to QML as a QImage.

        The ``_config`` argument is ignored (LiteContext only owns one device).
        QML invokes this on a Timer at ~1Hz from MirrorImage.qml.
        """
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
        try:
            self.device.click(int(x), int(y), control_check=False, control_name='ToolsClick')
        except Exception:
            logger.exception('LiteContext.click failed')

    @Slot(int, int, int)
    def long_click(self, x: int, y: int, duration_ms: int) -> None:
        try:
            seconds = max(0.05, float(duration_ms) / 1000.0)
            self.device.long_click(int(x), int(y), duration=(seconds, seconds + 0.1),
                                   control_name='ToolsLongClick')
        except Exception:
            logger.exception('LiteContext.long_click failed')

    @Slot(int, int, int, int, int)
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int) -> None:
        try:
            seconds = max(0.05, float(duration_ms) / 1000.0)
            self.device.swipe(p1=(int(x1), int(y1)), p2=(int(x2), int(y2)),
                              duration=(seconds, seconds + 0.05),
                              control_name='ToolsSwipe',
                              distance_check=False)
        except Exception:
            logger.exception('LiteContext.swipe failed')

    @Slot(str, str, result='QString')
    def test_ocr(self, roi: str, mode: str) -> str:
        """Run OCR over the given ROI on a fresh screenshot. mode in
        {Full,Single,Digit,DigitCounter,Duration,Quantity}. Returns JSON."""
        from module.atom.ocr import RuleOcr
        bbox = self._parse_roi(roi)
        if bbox is None:
            return json.dumps({'ok': False, 'error': 'bad roi'})
        try:
            rule = RuleOcr(roi=bbox, area=bbox, mode=mode or 'Full',
                           method='Default', keyword='', name='tools_test')
            img = self.device.screenshot()
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
        against the live screenshot inside ``roi_back``. Returns JSON
        ``{ok, found, score, x, y}``."""
        from module.atom.image import RuleImage
        front = self._parse_roi(roi_front)
        back = self._parse_roi(roi_back)
        if front is None or back is None:
            return json.dumps({'ok': False, 'error': 'bad roi'})
        if not file_path or not os.path.exists(file_path):
            return json.dumps({'ok': False, 'error': 'file not found'})
        try:
            rule = RuleImage(roi_front=front, roi_back=back,
                             threshold=float(threshold or 0.8),
                             method='Template matching', file=file_path)
            img = self.device.screenshot()
            found = bool(rule.match(img))
            return json.dumps({'ok': True, 'found': found})
        except Exception as e:
            logger.exception('LiteContext.test_image_match failed')
            return json.dumps({'ok': False, 'error': str(e)})
