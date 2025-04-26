from pathlib import Path

from qgis.core import QgsGradientFillSymbolLayer, QgsVectorLayer
from qgis.gui import QgsGradientFillSymbolLayerWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    widget = QgsGradientFillSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsGradientFillSymbolLayer(QColor(240, 175, 25), QColor(130, 0, 25)))

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "gradientfillsymbollayerwidget.png").as_posix())

    return {
        "gradientfillsymbollayerwidget.png": "QgsGradientFillSymbolLayerWidget in a default state"
    }
