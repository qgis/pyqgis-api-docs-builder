from pathlib import Path

from qgis.gui import QgsSymbolAnimationSettingsDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsSymbolAnimationSettingsDialog()

    im = ScreenshotUtils.capture_dialog(widget, width=590, height=200)
    im.save((dest_path / "symbolanimationsettingsdialog.png").as_posix())

    return {"symbolanimationsettingsdialog.png": "QgsSymbolAnimationSettingsDialog"}
