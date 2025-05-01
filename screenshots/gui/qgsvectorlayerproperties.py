from pathlib import Path

from qgis.core import QgsVectorLayer
from qgis.gui import QgsMapCanvas, QgsMessageBar, QgsVectorLayerProperties

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    uri = "point?crs=epsg:4326&field=id:integer"
    layer = QgsVectorLayer(uri, "Scratch point layer", "memory")
    canvas = QgsMapCanvas()
    messagebar = QgsMessageBar()
    dlg = QgsVectorLayerProperties(canvas, messagebar, layer)

    dlg.setCurrentPage("mOptsPage_Information")
    im = ScreenshotUtils.capture_dialog(dlg, width=790, height=700)
    im.save((dest_path / "vectorlayerpropertiesinformation.png").as_posix())

    dlg.setCurrentPage("mOptsPage_Source")
    im = ScreenshotUtils.capture_dialog(dlg, width=790, height=700)
    im.save((dest_path / "vectorlayerpropertiessource.png").as_posix())

    return {
        "vectorlayerpropertiesinformation.png": "QgsVectorLayerProperties showing the 'Information' page",
        "vectorlayerpropertiessource.png": "QgsVectorLayerProperties showing the 'Source' page",
    }
