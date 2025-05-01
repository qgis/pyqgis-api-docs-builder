from pathlib import Path

from qgis.gui import QgsSettingsTreeWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsSettingsTreeWidget()

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "settingstreewidget.png").as_posix())

    return {"settingstreewidget.png": "QgsSettingsTreeWidget"}
