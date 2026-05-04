# This Python file uses the following encoding: utf-8
"""
Lightweight Tools-only launcher (and a quick rule-debug helper).

Two ways to use this file:

1. **GUI launcher (default)** — run ``python tools_gui.py``. Same QML rule
   editors as ``gui.py``'s "Tools" menu, but skips the ProcessManager / per-
   config ScriptProcess machinery for a much faster start.

2. **Headless rule debug** — replace the body of ``if __name__ == '__main__'``
   below with calls to ``detect_image(...)`` / ``detect_ocr(...)``. No GUI
   spins up, no emulator is touched. Example::

        IMAGE_FILE = r"C:\\Users\\me\\Desktop\\shot.png"

        if __name__ == '__main__':
            from tasks.RichMan.script_task import ScriptTask
            target = ScriptTask.I_MALL_BONDLINGS_SURE
            print(detect_image(IMAGE_FILE, target))

The constants right below this docstring are the primary control surface —
edit them in place rather than reaching for a separate config file. Optional
CLI flags (``--image / --config / --no-warmup``) override the constants when
present so you can keep your default in the script and still flip behavior
from the shell occasionally.
"""
from __future__ import annotations

# ============================================================================
# Edit these to control how the launcher starts.
# ============================================================================

# Path to a screenshot. When non-empty, the GUI runs in **static-image mode**:
# Device is never initialized, no ADB is touched, ``gui_mirror_image`` returns
# this image, and ``test_ocr`` / ``test_image_match`` run against it.
# Empty string = live mode (connect to emulator on first screenshot).
IMAGE_FILE: str = r""

# Config name under config/ to bind Device to (without .json). Empty string
# means "first non-template config in config/". Only consulted in live mode.
CONFIG_NAME: str = ""

# Initial tool tab the QML window opens to (Chinese label). Empty falls back
# to "图像规则". Valid values: 图像规则 / 文字识别 / 点击规则 / 长按规则 /
# 滑动规则 / 列表规则.
DEFAULT_TOOL: str = ""

# ============================================================================

import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union

import cv2
import numpy as np
from PySide6.QtCore import QObject, Slot

from module.gui.context.lite_manager import LiteContext
from module.gui.fluent_app import FluentApp
from module.gui.register_type.paint_image import PaintImage
from module.gui.register_type.rule_file import RuleFile
from module.gui.utils import get_work_path
from module.logger import logger
from module.ocr.rpc import ensure_ocr_server_started


# ----------------------------------------------------------------------------
# Headless rule-debug helpers
# ----------------------------------------------------------------------------

def _load_image(image_or_path: Union[str, np.ndarray]) -> np.ndarray:
    """Accept either an existing numpy RGB array or a path to a PNG/JPG and
    return an RGB uint8 array — the same format ``Device.screenshot()`` would
    have produced, so the rule classes do not see any difference.

    Uses ``np.fromfile`` + ``cv2.imdecode`` so non-ASCII paths (Chinese, etc.)
    work on Windows where ``cv2.imread`` mishandles them.
    """
    if isinstance(image_or_path, np.ndarray):
        return image_or_path
    if not image_or_path:
        raise ValueError('image path is empty')
    abs_path = os.path.abspath(image_or_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(abs_path)
    buf = np.fromfile(abs_path, dtype=np.uint8)
    bgr = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if bgr is None:
        raise RuntimeError(f'cv2 failed to decode {abs_path}')
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def detect_image(image_or_path: Union[str, np.ndarray],
                 rule,
                 threshold: Optional[float] = None) -> Dict[str, Any]:
    """Run a ``RuleImage`` against a saved screenshot.

    Args:
        image_or_path: path to PNG/JPG, or an RGB numpy array.
        rule: any ``RuleImage`` (e.g. ``ScriptTask.I_FOO`` from a task's
              ``assets.py``).
        threshold: optional override for ``rule.threshold``.

    Returns a dict::

        {
          'matched':     bool,
          'name':        str,                # rule.name
          'threshold':   float,              # threshold actually used
          'roi_front':   tuple|None,         # match top-left + size, if matched
        }

    Note: ``RuleImage.match`` mutates ``rule.roi_front`` on hit. If you plan to
    reuse the same rule instance afterwards, snapshot ``roi_front`` first.
    """
    img = _load_image(image_or_path)
    used_threshold = threshold if threshold is not None else rule.threshold
    matched = bool(rule.match(img, threshold=threshold))
    return {
        'matched': matched,
        'name': getattr(rule, 'name', str(rule)),
        'threshold': used_threshold,
        'roi_front': tuple(rule.roi_front) if matched else None,
    }


def detect_ocr(image_or_path: Union[str, np.ndarray], rule):
    """Run a ``RuleOcr`` against a saved screenshot.

    Returns whatever the OCR mode produces (str for Full/Single, int for
    Digit/Quantity, ``(current, remain, total)`` for DigitCounter, etc.).
    """
    img = _load_image(image_or_path)
    return rule.ocr(img)


# ----------------------------------------------------------------------------
# GUI launcher
# ----------------------------------------------------------------------------

class _StubAddConfig(QObject):
    """Minimal stand-in for module.gui.context.add.Add — only needed so QML
    that calls ``add_config.all_script_files()`` does not crash."""

    @Slot(result='QVariantList')
    def all_script_files(self):
        config_dir = Path.cwd() / 'config'
        if not config_dir.exists():
            return []
        return [p.stem for p in config_dir.glob('*.json') if p.stem != 'template']

    @Slot(result='QVariantList')
    def all_json_file(self):
        return self.all_script_files()


def main() -> int:
    parser = argparse.ArgumentParser(
        description='OAS Tools-only launcher. The IMAGE_FILE / CONFIG_NAME / '
                    'DEFAULT_TOOL constants at the top of this file are the '
                    'primary control surface; flags below override them.')
    parser.add_argument('--config', '-c', default=None,
                        help='Override CONFIG_NAME constant.')
    parser.add_argument('--image', '-i', default=None,
                        help='Override IMAGE_FILE constant. When non-empty, '
                             'runs in static-image mode (no ADB).')
    parser.add_argument('--no-warmup', action='store_true',
                        help='Skip eager Device init on startup.')
    args = parser.parse_args()

    # CLI flag (when explicitly given) overrides the top-of-file constant.
    config_name = args.config if args.config is not None else (CONFIG_NAME or None)
    image_path = args.image if args.image is not None else (IMAGE_FILE or None)
    initial_tool = DEFAULT_TOOL or None

    if image_path and not os.path.exists(image_path):
        logger.error(f'image {image_path!r} does not exist; aborting')
        return 2

    # OCR server must be up before any RuleOcr.ocr() call (it talks to the
    # zerorpc OCR daemon on port 22268). Booting it here so the user does not
    # see a long pause when they first hit the Ocr Rule panel.
    ensure_ocr_server_started()

    app = FluentApp()
    lite = LiteContext(
        config_name=config_name,
        image_path=image_path,
        default_tool=initial_tool,
    )
    setting_ctx = _import_or_default()  # MainEvent.qml needs setting.read/update

    app.set_context_property(lite, 'process_manager')
    app.set_context_property(setting_ctx, 'setting')
    app.set_context_property(_StubAddConfig(), 'add_config')
    app.set_context_property(_make_utils(), 'utils')
    app.qml_register_type(PaintImage, 'PaintImage')
    app.qml_register_type(RuleFile, 'RuleFile')

    qml_path = Path(get_work_path()) / 'module' / 'gui' / 'qml' / 'tools_app.qml'
    FluentApp.engine.load(os.fspath(qml_path))
    if not FluentApp.engine.rootObjects():
        logger.error(f'Failed to load {qml_path}')
        return -1

    # Static mode: nothing to warm up (no Device). Otherwise schedule warmup
    # *after* the event loop starts so the window can paint before Device
    # init blocks for a moment.
    if not args.no_warmup and not lite.static_mode:
        from PySide6.QtCore import QTimer
        QTimer.singleShot(50, lite.warmup)

    return FluentApp.app.exec()


def _import_or_default():
    """Use the real Setting if available; otherwise fall back to an in-memory
    stub. Setting reads ``module/config/argument/setting.json`` which may not
    exist on a fresh checkout — Setting.copy_from_template handles that."""
    try:
        from module.gui.context.settings import Setting
        return Setting()
    except Exception:
        logger.exception('Failed to import Setting; using empty stub')

        class _StubSetting(QObject):
            @Slot(result='QString')
            def read(self):
                return '{}'

            @Slot(str)
            def update(self, _data):
                pass

        return _StubSetting()


def _make_utils():
    """Reuse module.gui.context.utils.Utils so test_notify still works."""
    try:
        from module.gui.context.utils import Utils
        return Utils()
    except Exception:
        logger.exception('Failed to import Utils; using empty stub')

        class _StubUtils(QObject):
            @Slot(result='QString')
            def current_datetime(self):
                from datetime import datetime
                return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return _StubUtils()


if __name__ == '__main__':
    # Default: launch the lite GUI honoring the constants above.
    sys.exit(main())

    # ---- Or: quick headless rule debug. Comment out the line above and
    # ---- uncomment one of the blocks below. Pick any RuleImage / RuleOcr
    # ---- attribute from a task's assets.py.
    #
    # from tasks.RichMan.script_task import ScriptTask
    # target = ScriptTask.I_MALL_BONDLINGS_SURE
    # print(detect_image(IMAGE_FILE, target))
    #
    # from tasks.KekkaiActivation.assets import KekkaiActivationAssets
    # target = KekkaiActivationAssets.O_CARD_ALL_TIME
    # print(detect_ocr(IMAGE_FILE, target))
