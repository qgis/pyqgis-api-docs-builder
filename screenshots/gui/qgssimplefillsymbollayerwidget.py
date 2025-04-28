from pathlib import Path

from qgis.core import QgsSimpleFillSymbolLayer, QgsVectorLayer
from qgis.gui import QgsSimpleFillSymbolLayerWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    widget = QgsSimpleFillSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsSimpleFillSymbolLayer(QColor(240, 175, 25)))

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "simplefillsymbollayerwidget.png").as_posix())

    return {"simplefillsymbollayerwidget.png": "QgsSimpleFillSymbolLayerWidget"}
