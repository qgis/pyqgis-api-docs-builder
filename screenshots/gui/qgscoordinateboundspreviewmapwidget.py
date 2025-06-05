from pathlib import Path

from qgis.core import QgsCoordinateReferenceSystem
from qgis.gui import QgsCoordinateBoundsPreviewMapWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCoordinateBoundsPreviewMapWidget()
    crs = QgsCoordinateReferenceSystem("EPSG:3035")
    rect = crs.bounds()
    widget.setPreviewRect(rect)

    im = ScreenshotUtils.capture_widget(widget, width=400, height=300)
    im.save((dest_path / "coordinateboundspreviewmapwidget.png").as_posix())

    return {"coordinateboundspreviewmapwidget.png": "QgsCoordinateBoundsPreviewMapWidget"}
