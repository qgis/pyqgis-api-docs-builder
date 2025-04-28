from pathlib import Path

from qgis.core import QgsHashedLineSymbolLayer, QgsVectorLayer
from qgis.gui import QgsHashedLineSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("LineString", "A line layer", "memory")
    widget = QgsHashedLineSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsHashedLineSymbolLayer())

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "hashedlinesymbollayerwidget.png").as_posix())

    return {"hashedlinesymbollayerwidget.png": "QgsHashedLineSymbolLayerWidget in a default state"}
