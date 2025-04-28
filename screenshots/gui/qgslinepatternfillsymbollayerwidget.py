from pathlib import Path

from qgis.core import QgsLinePatternFillSymbolLayer, QgsVectorLayer
from qgis.gui import QgsLinePatternFillSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Linestring", "Line Layer", "memory")
    widget = QgsLinePatternFillSymbolLayerWidget(layer)

    symbol_layer = QgsLinePatternFillSymbolLayer()
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "linepatternfillsymbollayerwidget.png").as_posix())

    return {"linepatternfillsymbollayerwidget.png": "QgsLinePatternFillSymbolLayerWidget"}
