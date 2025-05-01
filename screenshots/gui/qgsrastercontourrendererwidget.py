from pathlib import Path

from qgis.core import QgsRasterLayer
from qgis.gui import QgsRasterContourRendererWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "dem.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")

    widget = QgsRasterContourRendererWidget(layer)

    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "rastercontourrendererwidget.png").as_posix())

    return {"rastercontourrendererwidget.png": "QgsRasterContourRendererWidget"}
