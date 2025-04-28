from pathlib import Path

from qgis.core import QgsVectorFieldSymbolLayer, QgsVectorLayer
from qgis.gui import QgsVectorFieldSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point?field=x_coord:real&field=y_coord:real", "Point Layer", "memory")
    widget = QgsVectorFieldSymbolLayerWidget(layer)

    symbol_layer = QgsVectorFieldSymbolLayer()
    symbol_layer.setXAttribute("x_coord")
    symbol_layer.setYAttribute("y_coord")
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "vectorfieldsymbollayerwidget.png").as_posix())

    return {"vectorfieldsymbollayerwidget.png": "QgsVectorFieldSymbolLayerWidget"}
