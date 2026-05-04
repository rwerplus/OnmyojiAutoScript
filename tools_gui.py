# This Python file uses the following encoding: utf-8
"""
Lightweight Tools-only launcher.

Launches the same QML rule editors (Image / Ocr / Click / LongClick / Swipe /
List Rule) that live behind the ``Tools`` menu of ``gui.py``, but skips the
``ProcessManager`` / per-config ``ScriptProcess`` machinery — everything runs
in-process against a single ``Device``. That cuts startup from ~10 s with N
configs to ~3 s regardless of how many configs exist on disk.

Usage::

    python tools_gui.py                # auto-pick first non-template config
    python tools_gui.py --config oas   # use config/oas.json for Device wiring
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from PySide6.QtCore import QObject, Slot

from module.gui.context.lite_manager import LiteContext
from module.gui.fluent_app import FluentApp
from module.gui.register_type.paint_image import PaintImage
from module.gui.register_type.rule_file import RuleFile
from module.gui.utils import get_work_path
from module.logger import logger
from module.ocr.rpc import ensure_ocr_server_started


class _StubAddConfig(QObject):
    """Minimal stand-in for module.gui.context.add.Add — only needed so QML
    that calls ``add_config.all_script_files()`` does not crash. The Tools
    panel itself does not list configs, but Global/MainEvent.qml or other
    indirectly-loaded QML may probe these slots."""

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
    parser = argparse.ArgumentParser(description='OAS Tools-only launcher')
    parser.add_argument('--config', '-c', default=None,
                        help='Config name under config/ to bind Device to '
                             '(without .json). Defaults to first non-template.')
    parser.add_argument('--no-warmup', action='store_true',
                        help='Skip eager Device init on startup.')
    args = parser.parse_args()

    # OCR server must be up before any RuleOcr.ocr() call (it talks to the
    # zerorpc OCR daemon on port 22268). Booting it here so the user does not
    # see a long pause when they first hit the Ocr Rule panel.
    ensure_ocr_server_started()

    app = FluentApp()
    lite = LiteContext(config_name=args.config)
    setting_ctx = _import_or_default()  # MainEvent.qml needs setting.read/update

    # Register the contexts QML refers to. ``setting``, ``translator``, ``dpi``
    # are required by Global/MainEvent.qml's onCompleted handler.
    app.set_context_property(lite, 'process_manager')
    app.set_context_property(setting_ctx, 'setting')
    app.set_context_property(_StubAddConfig(), 'add_config')
    app.set_context_property(_make_utils(), 'utils')
    app.qml_register_type(PaintImage, 'PaintImage')
    app.qml_register_type(RuleFile, 'RuleFile')

    # Load our trimmed top-level QML instead of app.qml -> MainWindow.qml.
    qml_path = Path(get_work_path()) / 'module' / 'gui' / 'qml' / 'tools_app.qml'
    FluentApp.engine.load(os.fspath(qml_path))
    if not FluentApp.engine.rootObjects():
        logger.error(f'Failed to load {qml_path}')
        return -1

    if not args.no_warmup:
        # Schedule warmup *after* the event loop starts so the window can
        # paint before Device init blocks for a moment.
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
    sys.exit(main())
