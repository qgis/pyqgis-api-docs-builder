from pathlib import Path

from qgis.core import QgsEllipseSymbolLayer, QgsVectorLayer
from qgis.gui import QgsEllipseSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    widget = QgsEllipseSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsEllipseSymbolLayer())

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "ellipsesymbollayerwidget.png").as_posix())

    return {"ellipsesymbollayerwidget.png": "QgsEllipseSymbolLayerWidget in a default state"}
