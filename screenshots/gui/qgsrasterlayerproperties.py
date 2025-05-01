from pathlib import Path

from qgis.core import QgsRasterLayer
from qgis.gui import QgsMapCanvas, QgsMessageBar, QgsRasterLayerProperties

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "dem.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")

    canvas = QgsMapCanvas()
    messagebar = QgsMessageBar()
    dlg = QgsRasterLayerProperties(layer, canvas, messagebar)

    dlg.setCurrentPage("mOptsPage_Information")
    im = ScreenshotUtils.capture_dialog(dlg, width=790, height=700)
    im.save((dest_path / "rasterlayerpropertiesinformation.png").as_posix())

    dlg.setCurrentPage("mOptsPage_Source")
    im = ScreenshotUtils.capture_dialog(dlg, width=790, height=700)
    im.save((dest_path / "rasterlayerpropertiessource.png").as_posix())

    return {
        "rasterlayerpropertiesinformation.png": "QgsRasterLayerProperties showing the 'Information' page",
        "rasterlayerpropertiessource.png": "QgsRasterLayerProperties showing the 'Source' page",
    }
