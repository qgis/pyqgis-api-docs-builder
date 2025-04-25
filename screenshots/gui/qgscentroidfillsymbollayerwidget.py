from pathlib import Path

from qgis.core import QgsCentroidFillSymbolLayer, QgsVectorLayer
from qgis.gui import QgsCentroidFillSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    widget = QgsCentroidFillSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsCentroidFillSymbolLayer())

    im = ScreenshotUtils.capture_widget(widget, width=590, height=150)
    im.save((dest_path / "centroidfillsymbollayerwidget.png").as_posix())

    return {
        "centroidfillsymbollayerwidget.png": "QgsCentroidFillSymbolLayerWidget in a default state"
    }
