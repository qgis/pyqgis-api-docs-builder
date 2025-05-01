from pathlib import Path

from qgis.core import QgsContrastEnhancement, QgsMultiBandColorRenderer, QgsRasterLayer
from qgis.gui import QgsMultiBandColorRendererWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "landsat.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")
    red_contrast = QgsContrastEnhancement()
    red_contrast.setMinimumValue(0)
    red_contrast.setMaximumValue(255)
    renderer = QgsMultiBandColorRenderer(layer.dataProvider(), 1, 2, 3)
    renderer.setRedContrastEnhancement(red_contrast)
    green_contrast = QgsContrastEnhancement()
    green_contrast.setMinimumValue(5)
    green_contrast.setMaximumValue(250)
    renderer.setGreenContrastEnhancement(green_contrast)
    blue_contrast = QgsContrastEnhancement()
    blue_contrast.setMinimumValue(15)
    blue_contrast.setMaximumValue(200)
    renderer.setBlueContrastEnhancement(blue_contrast)

    layer.setRenderer(renderer)
    widget = QgsMultiBandColorRendererWidget(layer)

    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "multibandcolorrendererwidget.png").as_posix())

    return {"multibandcolorrendererwidget.png": "QgsMultiBandColorRendererWidget"}
