from pathlib import Path

from qgis.core import QgsMaskMarkerSymbolLayer, QgsVectorLayer
from qgis.gui import QgsMaskMarkerSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    widget = QgsMaskMarkerSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsMaskMarkerSymbolLayer())

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "maskmarkersymbollayerwidget.png").as_posix())

    return {"maskmarkersymbollayerwidget.png": "QgsMaskMarkerSymbolLayerWidget"}
