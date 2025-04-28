from pathlib import Path

from qgis.core import QgsMarkerLineSymbolLayer, QgsVectorLayer
from qgis.gui import QgsMarkerLineSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("LineString", "A line layer", "memory")
    widget = QgsMarkerLineSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsMarkerLineSymbolLayer())

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "markerlinesymbollayerwidget.png").as_posix())

    return {"markerlinesymbollayerwidget.png": "QgsMarkerLineSymbolLayerWidget in a default state"}
