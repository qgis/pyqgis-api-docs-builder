from pathlib import Path

from qgis.core import QgsLineburstSymbolLayer, QgsVectorLayer
from qgis.gui import QgsLineburstSymbolLayerWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Linestring", "Line Layer", "memory")
    widget = QgsLineburstSymbolLayerWidget(layer)

    symbol_layer = QgsLineburstSymbolLayer()
    symbol_layer.setColor(QColor(120, 185, 15))
    symbol_layer.setColor2(QColor(215, 190, 65))
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "lineburstsymbollayerwidget.png").as_posix())

    return {"lineburstsymbollayerwidget.png": "QgsLineburstSymbolLayerWidget"}
