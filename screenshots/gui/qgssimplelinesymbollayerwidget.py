from pathlib import Path

from qgis.core import QgsSimpleLineSymbolLayer, QgsVectorLayer
from qgis.gui import QgsSimpleLineSymbolLayerWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Linestring", "A line layer", "memory")
    widget = QgsSimpleLineSymbolLayerWidget(layer)

    simple_layer = QgsSimpleLineSymbolLayer(QColor(240, 175, 25))
    widget.setSymbolLayer(simple_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "simplelinesymbollayerwidget.png").as_posix())

    return {"simplelinesymbollayerwidget.png": "QgsSimpleLineSymbolLayerWidget"}
