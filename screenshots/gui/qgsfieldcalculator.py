from pathlib import Path

from qgis.core import QgsVectorLayer
from qgis.gui import QgsFieldCalculator

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    uri = "point?crs=epsg:4326&field=id:integer"
    layer = QgsVectorLayer(uri, "Scratch point layer", "memory")
    layer.startEditing()
    dlg = QgsFieldCalculator(layer)

    im = ScreenshotUtils.capture_dialog(dlg, width=790, height=700)
    im.save((dest_path / "fieldcalculator.png").as_posix())

    return {"fieldcalculator.png": "QgsFieldCalculator"}
