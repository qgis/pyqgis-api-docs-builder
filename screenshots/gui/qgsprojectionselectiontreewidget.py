from pathlib import Path

from qgis.core import QgsApplication, QgsCoordinateReferenceSystem, QgsRectangle
from qgis.gui import QgsProjectionSelectionTreeWidget

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

    widget = QgsProjectionSelectionTreeWidget()
    crs = QgsCoordinateReferenceSystem.fromEpsgId(4326)
    widget.setCrs(crs)
    widget.setPreviewRect(QgsRectangle(7.58, -38.16, 76.34, 39.08))

    im = ScreenshotUtils.capture_widget(widget, width=600, height=700)
    im.save((dest_path / "projectionselectiontreewidget.png").as_posix())

    return {"projectionselectiontreewidget.png": "QgsProjectionSelectionTreeWidget"}
