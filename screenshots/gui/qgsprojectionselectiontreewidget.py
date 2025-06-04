from pathlib import Path

from qgis.core import QgsCoordinateReferenceSystem
from qgis.gui import QgsProjectionSelectionTreeWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsProjectionSelectionTreeWidget()
    crs = QgsCoordinateReferenceSystem.fromEpsgId(4326)
    widget.setCrs(crs)

    im = ScreenshotUtils.capture_widget(widget, width=600, height=700)
    im.save((dest_path / "projectionselectiontreewidget.png").as_posix())

    return {"projectionselectiontreewidget.png": "QgsProjectionSelectionTreeWidget"}
