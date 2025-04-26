from pathlib import Path

from qgis.core import QgsFontMarkerSymbolLayer, QgsVectorLayer
from qgis.gui import QgsFontMarkerSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    widget = QgsFontMarkerSymbolLayerWidget(layer)

    widget.setSymbolLayer(QgsFontMarkerSymbolLayer())

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "fontmarkersymbollayerwidget.png").as_posix())

    return {"fontmarkersymbollayerwidget.png": "QgsFontMarkerSymbolLayerWidget in a default state"}
