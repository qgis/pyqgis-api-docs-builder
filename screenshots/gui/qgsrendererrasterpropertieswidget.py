from pathlib import Path

from qgis.core import QgsRasterLayer
from qgis.gui import QgsMapCanvas, QgsRendererRasterPropertiesWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "dem.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")

    canvas = QgsMapCanvas()
    widget = QgsRendererRasterPropertiesWidget(layer, canvas)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "rendererrasterpropertieswidget.png").as_posix())

    return {"rendererrasterpropertieswidget.png": "QgsRendererRasterPropertiesWidget"}
