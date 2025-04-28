from pathlib import Path

from qgis.core import QgsLinearReferencingSymbolLayer, QgsVectorLayer
from qgis.gui import QgsLinearReferencingSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Linestring", "Line Layer", "memory")
    widget = QgsLinearReferencingSymbolLayerWidget(layer)

    symbol_layer = QgsLinearReferencingSymbolLayer()
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "linearreferencingsymbollayerwidget.png").as_posix())

    return {"linearreferencingsymbollayerwidget.png": "QgsLinearReferencingSymbolLayerWidget"}
