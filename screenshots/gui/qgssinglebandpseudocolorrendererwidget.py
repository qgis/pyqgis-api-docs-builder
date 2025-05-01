from pathlib import Path

from qgis.core import (
    QgsColorRampShader,
    QgsGradientColorRamp,
    QgsRasterLayer,
    QgsRasterShader,
    QgsSingleBandPseudoColorRenderer,
)
from qgis.gui import QgsSingleBandPseudoColorRendererWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "dem.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")

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
    renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, raster_shader)
    layer.setRenderer(renderer)

    widget = QgsSingleBandPseudoColorRendererWidget(layer)

    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "singlebandpsuedocolorrendererwidget.png").as_posix())

    return {"singlebandpsuedocolorrendererwidget.png": "QgsSingleBandPseudoColorRendererWidget"}
