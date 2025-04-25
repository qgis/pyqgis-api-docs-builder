from pathlib import Path

from qgis.core import QgsAnimatedMarkerSymbolLayer, QgsVectorLayer
from qgis.gui import QgsAnimatedMarkerSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    widget = QgsAnimatedMarkerSymbolLayerWidget(layer)

    image_path = (Path(__file__).parent / ".." / "resources" / "qgis_logo_animated.gif").as_posix()

    widget.setSymbolLayer(QgsAnimatedMarkerSymbolLayer(image_path))

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "animatedmarkersymbollayerwidget.png").as_posix())

    return {"animatedmarkersymbollayerwidget.png": "QgsAnimatedMarkerSymbolLayerWidget"}
