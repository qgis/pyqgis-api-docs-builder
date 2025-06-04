from pathlib import Path

from qgis.core import QgsCoordinateReferenceSystem
from qgis.gui import QgsProjectionSelectionDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    dialog = QgsProjectionSelectionDialog()
    crs = QgsCoordinateReferenceSystem.fromEpsgId(4326)
    dialog.setCrs(crs)

    im = ScreenshotUtils.capture_dialog(dialog, width=600, height=700)
    im.save((dest_path / "projectionselectiondialog.png").as_posix())

    return {"projectionselectiondialog.png": "QgsProjectionSelectionDialog"}
