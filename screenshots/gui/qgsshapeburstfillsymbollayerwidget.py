from pathlib import Path

from qgis.core import QgsShapeburstFillSymbolLayer, QgsVectorLayer
from qgis.gui import QgsShapeburstFillSymbolLayerWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    widget = QgsShapeburstFillSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsShapeburstFillSymbolLayer(QColor(240, 175, 25), QColor(130, 0, 25)))

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "shapeburstfillsymbollayerwidget.png").as_posix())

    return {"shapeburstfillsymbollayerwidget.png": "QgsShapeburstFillSymbolLayerWidget"}
