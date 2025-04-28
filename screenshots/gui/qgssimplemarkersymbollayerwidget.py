from pathlib import Path

from qgis.core import QgsSimpleMarkerSymbolLayer, QgsVectorLayer
from qgis.gui import QgsSimpleMarkerSymbolLayerWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    widget = QgsSimpleMarkerSymbolLayerWidget(layer)

    simple_layer = QgsSimpleMarkerSymbolLayer()
    simple_layer.setColor(QColor(240, 175, 25))
    widget.setSymbolLayer(simple_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "simplemarkersymbollayerwidget.png").as_posix())

    return {"simplemarkersymbollayerwidget.png": "QgsSimpleMarkerSymbolLayerWidget"}
