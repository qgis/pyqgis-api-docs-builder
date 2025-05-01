from pathlib import Path

from qgis.core import QgsRasterLayer
from qgis.gui import QgsRasterHistogramWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "dem.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")

    widget = QgsRasterHistogramWidget(layer)
    widget.setSelectedBand(1)
    widget.computeHistogram(True)
    widget.refreshHistogram()

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "rasterhistogramwidget.png").as_posix())

    return {"rasterhistogramwidget.png": "QgsRasterHistogramWidget"}
