from pathlib import Path

from qgis.core import QgsRasterFillSymbolLayer, QgsVectorLayer
from qgis.gui import QgsRasterFillSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "Polygon Layer", "memory")
    widget = QgsRasterFillSymbolLayerWidget(layer)

    image_path = (Path(__file__).parent / ".." / "resources" / "qgis_logo_animated.gif").as_posix()

    symbol_layer = QgsRasterFillSymbolLayer(image_path)
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, height=600, padding=0)
    im.save((dest_path / "rasterfillsymbollayerwidget.png").as_posix())

    return {"rasterfillsymbollayerwidget.png": "QgsRasterFillSymbolLayerWidget"}
