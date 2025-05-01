from pathlib import Path

from qgis.core import QgsMeshLayer
from qgis.gui import QgsMapCanvas, QgsMeshLayerProperties, QgsMessageBar

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "quad_flower.2dm").as_posix()
    layer = QgsMeshLayer(layer_path, "Mesh Layer", "mdal")

    canvas = QgsMapCanvas()
    messagebar = QgsMessageBar()
    dlg = QgsMeshLayerProperties(layer, canvas, messagebar)

    dlg.setCurrentPage("mOptsPage_Information")
    im = ScreenshotUtils.capture_dialog(dlg, width=790, height=700)
    im.save((dest_path / "meshlayerpropertiesinformation.png").as_posix())

    dlg.setCurrentPage("mOptsPage_Source")
    im = ScreenshotUtils.capture_dialog(dlg, width=790, height=700)
    im.save((dest_path / "meshlayerpropertiessource.png").as_posix())

    return {
        "meshlayerpropertiesinformation.png": "QgsMeshLayerProperties showing the 'Information' page",
        "meshlayerpropertiessource.png": "QgsMeshLayerProperties showing the 'Source' page",
    }
