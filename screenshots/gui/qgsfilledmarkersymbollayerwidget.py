from pathlib import Path

from qgis.core import QgsFilledMarkerSymbolLayer, QgsVectorLayer
from qgis.gui import QgsFilledMarkerSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    widget = QgsFilledMarkerSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsFilledMarkerSymbolLayer())

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "filledmarkersymbollayerwidget.png").as_posix())

    return {
        "filledmarkersymbollayerwidget.png": "QgsFilledMarkerSymbolLayerWidget in a default state"
    }
