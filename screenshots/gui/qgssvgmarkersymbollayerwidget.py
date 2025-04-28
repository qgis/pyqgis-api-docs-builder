from pathlib import Path

from qgis.core import QgsSvgMarkerSymbolLayer, QgsVectorLayer
from qgis.gui import QgsSvgMarkerSymbolLayerWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    widget = QgsSvgMarkerSymbolLayerWidget(layer)

    simple_layer = QgsSvgMarkerSymbolLayer("")
    simple_layer.setColor(QColor(240, 175, 25))
    widget.setSymbolLayer(simple_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "svgmarkersymbollayerwidget.png").as_posix())

    return {"svgmarkersymbollayerwidget.png": "QgsSvgMarkerSymbolLayerWidget"}
