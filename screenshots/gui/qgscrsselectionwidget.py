from pathlib import Path

from qgis.core import QgsApplication, QgsCoordinateReferenceSystem
from qgis.gui import QgsCrsSelectionWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    QgsApplication.coordinateReferenceSystemRegistry().clearRecent()
    QgsApplication.coordinateReferenceSystemRegistry().pushRecent(
        QgsCoordinateReferenceSystem("ESRI:54030")
    )
    QgsApplication.coordinateReferenceSystemRegistry().pushRecent(
        QgsCoordinateReferenceSystem("EPSG:3857")
    )
    QgsApplication.coordinateReferenceSystemRegistry().pushRecent(
        QgsCoordinateReferenceSystem("EPSG:4326")
    )

    widget = QgsCrsSelectionWidget()
    crs = QgsCoordinateReferenceSystem("EPSG:4326")
    widget.setCrs(crs)

    im = ScreenshotUtils.capture_widget(widget, width=600, height=700)
    im.save((dest_path / "crsselectionwidget.png").as_posix())

    return {"crsselectionwidget.png": "QgsCrsSelectionWidget"}
