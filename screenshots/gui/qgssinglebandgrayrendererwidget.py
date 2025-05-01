from pathlib import Path

from qgis.core import QgsRasterLayer
from qgis.gui import QgsSingleBandGrayRendererWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "dem.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")

    widget = QgsSingleBandGrayRendererWidget(layer)

    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "singlebandgrayrendererwidget.png").as_posix())

    return {"singlebandgrayrendererwidget.png": "QgsSingleBandGrayRendererWidget"}
