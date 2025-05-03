from pathlib import Path

from qgis.core import (
    QgsCategorizedSymbolRenderer,
    QgsColorRampShader,
    QgsFillSymbol,
    QgsGradientColorRamp,
    QgsLayerTreeModel,
    QgsLineSymbol,
    QgsMarkerSymbol,
    QgsProject,
    QgsRasterLayer,
    QgsRasterShader,
    QgsRendererCategory,
    QgsSingleBandPseudoColorRenderer,
    QgsSingleSymbolRenderer,
    QgsVectorLayer,
)
from qgis.gui import QgsLayerTreeView
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    p = QgsProject.instance()
    layer = QgsVectorLayer("LineString", "Lines", "memory")
    symbol = QgsLineSymbol.createSimple({})
    symbol.setColor(QColor(60, 90, 60))
    layer.setRenderer(QgsSingleSymbolRenderer(symbol))

    layer2 = QgsVectorLayer("Point", "Points", "memory")
    symbol = QgsMarkerSymbol.createSimple({})
    symbol.setColor(QColor(150, 0, 0))
    cat_1 = QgsRendererCategory("P", symbol.clone(), "Protected")
    symbol.setColor(QColor(230, 160, 10))
    cat_2 = QgsRendererCategory("I", symbol.clone(), "In progress")
    symbol.setColor(QColor(50, 140, 50))
    cat_3 = QgsRendererCategory("A", symbol.clone(), "Approved")
    renderer = QgsCategorizedSymbolRenderer("classification", [cat_1, cat_2, cat_3])
    symbol.setColor(QColor(240, 185, 20))
    renderer.setSourceSymbol(symbol.clone())
    layer2.setRenderer(renderer)

    layer3 = QgsVectorLayer("Polygon", "Polygons", "memory")
    symbol = QgsFillSymbol.createSimple({})
    symbol.setColor(QColor(60, 90, 60))
    layer3.setRenderer(QgsSingleSymbolRenderer(symbol))

    p.addMapLayers([layer, layer2, layer3])

    layer_path = (Path(__file__).parent / ".." / "resources" / "dem.tif").as_posix()
    raster_layer_1 = QgsRasterLayer(layer_path, "Raster Layer")
    ramp = QgsGradientColorRamp()
    shader = QgsColorRampShader(0, 1000, ramp)
    shader.setColorRampItemList(
        [
            QgsColorRampShader.ColorRampItem(0, ramp.color(0)),
            QgsColorRampShader.ColorRampItem(250, ramp.color(0.25)),
            QgsColorRampShader.ColorRampItem(500, ramp.color(0.5)),
            QgsColorRampShader.ColorRampItem(750, ramp.color(0.75)),
            QgsColorRampShader.ColorRampItem(1000, ramp.color(1.0)),
        ]
    )
    raster_shader = QgsRasterShader()
    raster_shader.setRasterShaderFunction(shader)
    renderer = QgsSingleBandPseudoColorRenderer(raster_layer_1.dataProvider(), 1, raster_shader)
    raster_layer_1.setRenderer(renderer)

    layer_path = (Path(__file__).parent / ".." / "resources" / "landsat.tif").as_posix()
    raster_layer_2 = QgsRasterLayer(layer_path, "Basemap Layer")
    p.addMapLayers([raster_layer_1, raster_layer_2], False)
    raster_group = p.layerTreeRoot().addGroup("Basemaps")
    raster_group.addLayer(raster_layer_1)
    raster_group.addLayer(raster_layer_2)

    model = QgsLayerTreeModel(p.layerTreeRoot())
    widget = QgsLayerTreeView()
    widget.setModel(model)

    im = ScreenshotUtils.capture_widget(widget, width=390, height=850, padding=0)
    im.save((dest_path / "layertreeview.png").as_posix())

    return {"layertreeview.png": "QgsLayerTreeView"}
