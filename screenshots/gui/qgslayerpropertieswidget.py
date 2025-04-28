from pathlib import Path

from qgis.core import QgsFillSymbol, QgsSimpleFillSymbolLayer, QgsVectorLayer
from qgis.gui import QgsLayerPropertiesWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    simple_fill = QgsSimpleFillSymbolLayer()
    simple_fill.setColor(QColor(120, 185, 15))
    symbol = QgsFillSymbol()
    symbol.changeSymbolLayer(0, simple_fill)
    widget = QgsLayerPropertiesWidget(simple_fill, symbol, layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "layerpropertieswidget.png").as_posix())

    return {
        "layerpropertieswidget.png": "QgsLayerPropertiesWidget showing a simple fill symbol layer"
    }
