from pathlib import Path

from qgis.core import QgsRasterMarkerSymbolLayer, QgsVectorLayer
from qgis.gui import QgsRasterMarkerSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "Point Layer", "memory")
    widget = QgsRasterMarkerSymbolLayerWidget(layer)

    image_path = (Path(__file__).parent / ".." / "resources" / "qgis_logo_animated.gif").as_posix()

    symbol_layer = QgsRasterMarkerSymbolLayer(image_path)
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, height=600, padding=0)
    im.save((dest_path / "rastermarkersymbollayerwidget.png").as_posix())

    return {"rastermarkersymbollayerwidget.png": "QgsRasterMarkerSymbolLayerWidget"}
