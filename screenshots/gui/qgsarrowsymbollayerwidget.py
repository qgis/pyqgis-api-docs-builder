from pathlib import Path

from qgis.core import QgsArrowSymbolLayer, QgsVectorLayer
from qgis.gui import QgsArrowSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("LineString", "A line layer", "memory")
    widget = QgsArrowSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsArrowSymbolLayer())

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "arrowsymbollayerwidget.png").as_posix())

    return {"arrowsymbollayerwidget.png": "QgsArrowSymbolLayerWidget in a default state"}
