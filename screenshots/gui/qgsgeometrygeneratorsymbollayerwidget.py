from pathlib import Path

from qgis.core import QgsGeometryGeneratorSymbolLayer, QgsVectorLayer
from qgis.gui import QgsGeometryGeneratorSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    widget = QgsGeometryGeneratorSymbolLayerWidget(layer)

    generator = QgsGeometryGeneratorSymbolLayer.create({})
    generator.setGeometryExpression("buffer(@geometry, 2)")
    widget.setSymbolLayer(generator)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "geometrygeneratorsymbollayerwidget.png").as_posix())

    return {
        "geometrygeneratorsymbollayerwidget.png": "QgsGeometryGeneratorSymbolLayerWidget in a default state"
    }
