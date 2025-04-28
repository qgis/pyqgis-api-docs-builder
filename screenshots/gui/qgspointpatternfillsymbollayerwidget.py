from pathlib import Path

from qgis.core import QgsPointPatternFillSymbolLayer, QgsVectorLayer
from qgis.gui import QgsPointPatternFillSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "Polygon Layer", "memory")
    widget = QgsPointPatternFillSymbolLayerWidget(layer)

    symbol_layer = QgsPointPatternFillSymbolLayer()
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "pointpatternfillsymbollayerwidget.png").as_posix())

    return {"pointpatternfillsymbollayerwidget.png": "QgsPointPatternFillSymbolLayerWidget"}
