from pathlib import Path

from qgis.gui import QgsLabelLineAnchorWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsLabelLineAnchorWidget()
    im = ScreenshotUtils.capture_widget(widget, width=390, height=700)
    im.save((dest_path / "labellineanchorwidget.png").as_posix())

    return {"labellineanchorwidget.png": "QgsLabelLineAnchorWidget"}
