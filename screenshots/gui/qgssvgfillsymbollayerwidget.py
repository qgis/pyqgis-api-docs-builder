from pathlib import Path

from qgis.core import QgsSVGFillSymbolLayer, QgsVectorLayer
from qgis.gui import QgsSVGFillSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "Polygon Layer", "memory")
    widget = QgsSVGFillSymbolLayerWidget(layer)

    symbol_layer = QgsSVGFillSymbolLayer("")
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "svgfillsymbollayerwidget.png").as_posix())

    return {"svgfillsymbollayerwidget.png": "QgsSVGFillSymbolLayerWidget"}
