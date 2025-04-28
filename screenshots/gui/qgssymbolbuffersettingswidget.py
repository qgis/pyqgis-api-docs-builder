from pathlib import Path

from qgis.gui import QgsSymbolBufferSettingsWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsSymbolBufferSettingsWidget()

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "symbolbuffersettingswidget.png").as_posix())

    return {"symbolbuffersettingswidget.png": "QgsSymbolBufferSettingsWidget"}
