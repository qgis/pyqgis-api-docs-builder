from pathlib import Path

from qgis.core import QgsProject, QgsVectorLayer
from qgis.gui import (
    QgsCustomLayerOrderWidget,
    QgsLayerTreeMapCanvasBridge,
    QgsMapCanvas,
)

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    p = QgsProject.instance()
    layer = QgsVectorLayer("LineString", "Lines", "memory")
    layer2 = QgsVectorLayer("Point", "Points", "memory")
    layer3 = QgsVectorLayer("Polygon", "Polygons", "memory")
    canvas = QgsMapCanvas()
    bridge = QgsLayerTreeMapCanvasBridge(p.layerTreeRoot(), canvas)

    widget = QgsCustomLayerOrderWidget(bridge)

    p.addMapLayers([layer, layer2, layer3])
    im = ScreenshotUtils.capture_widget(widget, width=390, height=250)
    im.save((dest_path / "customlayerorderwidgetdisabled.png").as_posix())

    p.layerTreeRoot().setHasCustomLayerOrder(True)
    p.layerTreeRoot().setCustomLayerOrder([layer3, layer, layer2])
    im = ScreenshotUtils.capture_widget(widget, width=390, height=250)
    im.save((dest_path / "customlayerorderwidgetenabled.png").as_posix())

    return {
        "customlayerorderwidgetdisabled.png": "QgsCustomLayerOrderWidget showing default state (no custom layer order)",
        "customlayerorderwidgetenabled.png": "QgsCustomLayerOrderWidget showing custom layer order",
    }
