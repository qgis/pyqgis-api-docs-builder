from pathlib import Path

from qgis.core import QgsCoordinateReferenceSystem
from qgis.gui import QgsCoordinateOperationWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCoordinateOperationWidget()
    source_crs = QgsCoordinateReferenceSystem("EPSG:27572")
    widget.setSourceCrs(source_crs)
    destination_crs = QgsCoordinateReferenceSystem("EPSG:2154")
    widget.setDestinationCrs(destination_crs)

    im = ScreenshotUtils.capture_widget(widget, width=800, height=700)
    im.save((dest_path / "coordinateoperationwidget.png").as_posix())

    return {"coordinateoperationwidget.png": "QgsCoordinateOperationWidget"}
