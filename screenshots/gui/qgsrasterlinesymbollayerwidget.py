from pathlib import Path

from qgis.core import QgsRasterLineSymbolLayer, QgsVectorLayer
from qgis.gui import QgsRasterLineSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Linestring", "Line Layer", "memory")
    widget = QgsRasterLineSymbolLayerWidget(layer)

    image_path = (Path(__file__).parent / ".." / "resources" / "qgis_logo_animated.gif").as_posix()

    symbol_layer = QgsRasterLineSymbolLayer(image_path)
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, height=600, padding=0)
    im.save((dest_path / "rasterlinesymbollayerwidget.png").as_posix())

    return {"rasterlinesymbollayerwidget.png": "QgsRasterLineSymbolLayerWidget"}
