from pathlib import Path

from qgis.core import QgsRandomMarkerFillSymbolLayer, QgsVectorLayer
from qgis.gui import QgsRandomMarkerFillSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "Polygon Layer", "memory")
    widget = QgsRandomMarkerFillSymbolLayerWidget(layer)

    symbol_layer = QgsRandomMarkerFillSymbolLayer()
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "randommarkerfillsymbollayerwidget.png").as_posix())

    return {"randommarkerfillsymbollayerwidget.png": "QgsRandomMarkerFillSymbolLayerWidget"}
