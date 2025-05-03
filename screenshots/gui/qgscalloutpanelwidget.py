from pathlib import Path

from qgis.gui import QgsCalloutPanelWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCalloutPanelWidget()
    im = ScreenshotUtils.capture_widget(widget, width=390, height=700)
    im.save((dest_path / "calloutpanelwidget.png").as_posix())

    return {"calloutpanelwidget.png": "QgsCalloutPanelWidget"}
