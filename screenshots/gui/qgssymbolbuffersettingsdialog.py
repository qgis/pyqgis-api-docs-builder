from pathlib import Path

from qgis.gui import QgsSymbolBufferSettingsDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsSymbolBufferSettingsDialog()

    im = ScreenshotUtils.capture_dialog(widget, width=590, height=200)
    im.save((dest_path / "symbolbuffersettingsdialog.png").as_posix())

    return {"symbolbuffersettingsdialog.png": "QgsSymbolBufferSettingsDialog"}
