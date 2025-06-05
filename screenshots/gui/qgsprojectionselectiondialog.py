from pathlib import Path

from qgis.core import QgsApplication, QgsCoordinateReferenceSystem
from qgis.gui import QgsProjectionSelectionDialog

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

    dialog = QgsProjectionSelectionDialog()
    crs = QgsCoordinateReferenceSystem.fromEpsgId(4326)
    dialog.setCrs(crs)

    im = ScreenshotUtils.capture_dialog(dialog, width=600, height=700)
    im.save((dest_path / "projectionselectiondialog.png").as_posix())

    return {"projectionselectiondialog.png": "QgsProjectionSelectionDialog"}
