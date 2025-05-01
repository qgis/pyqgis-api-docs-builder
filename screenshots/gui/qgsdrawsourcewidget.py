from pathlib import Path

from qgis.gui import QgsDrawSourceWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsDrawSourceWidget()

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "drawsourcewidget.png").as_posix())

    return {"drawsourcewidget.png": "QgsDrawSourceWidget"}
