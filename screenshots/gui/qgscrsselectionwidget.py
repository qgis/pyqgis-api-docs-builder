from pathlib import Path

from qgis.core import QgsCoordinateReferenceSystem
from qgis.gui import QgsCrsSelectionWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCrsSelectionWidget()
    crs = QgsCoordinateReferenceSystem.fromEpsgId(4326)
    widget.setCrs(crs)

    im = ScreenshotUtils.capture_widget(widget, width=600, height=700)
    im.save((dest_path / "crsselectionwidget.png").as_posix())

    return {"crsselectionwidget.png": "QgsCrsSelectionWidget"}
