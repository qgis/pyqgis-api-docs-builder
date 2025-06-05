from pathlib import Path

from qgis.core import QgsCoordinateReferenceSystem
from qgis.gui import QgsCrsDefinitionWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCrsDefinitionWidget()
    crs = QgsCoordinateReferenceSystem("EPSG:4326")
    widget.setCrs(crs)

    im = ScreenshotUtils.capture_widget(widget, width=600)
    im.save((dest_path / "crsdefinitionwidget.png").as_posix())

    return {"crsdefinitionwidget.png": "QgsCrsDefinitionWidget"}
