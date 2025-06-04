from pathlib import Path

from qgis.core import QgsCoordinateReferenceSystem
from qgis.gui import QgsProjectionSelectionWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsProjectionSelectionWidget()
    crs = QgsCoordinateReferenceSystem.fromEpsgId(4326)
    widget.setCrs(crs)

    im = ScreenshotUtils.capture_widget(widget)
    im.save((dest_path / "projectionselectionwidget.png").as_posix())

    return {"projectionselectionwidget.png": "QgsProjectionSelectionWidget"}
