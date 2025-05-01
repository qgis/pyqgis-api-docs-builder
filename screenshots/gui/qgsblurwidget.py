from pathlib import Path

from qgis.gui import QgsBlurWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsBlurWidget()

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "blurwidget.png").as_posix())

    return {"blurwidget.png": "QgsBlurWidget"}
