from pathlib import Path

from qgis.core import QgsFilledLineSymbolLayer, QgsVectorLayer
from qgis.gui import QgsFilledLineSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("LineString", "A line layer", "memory")
    widget = QgsFilledLineSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsFilledLineSymbolLayer())

    im = ScreenshotUtils.capture_widget(widget, width=590, height=150, padding=0)
    im.save((dest_path / "filledlinesymbollayerwidget.png").as_posix())

    return {"filledlinesymbollayerwidget.png": "QgsFilledLineSymbolLayerWidget in a default state"}
