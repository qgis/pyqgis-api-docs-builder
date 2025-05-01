from pathlib import Path

from qgis.core import QgsVectorTileLayer
from qgis.gui import QgsMapCanvas, QgsMessageBar, QgsVectorTileLayerProperties

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    vt_path = (Path(__file__).parent / ".." / "resources" / "mbtiles_vt.mbtiles").as_posix()
    layer = QgsVectorTileLayer(f"type=mbtiles&url={vt_path}", "Vector Tile Layer")
    canvas = QgsMapCanvas()
    messagebar = QgsMessageBar()
    dlg = QgsVectorTileLayerProperties(layer, canvas, messagebar)

    dlg.setCurrentPage("mOptsPage_Information")
    im = ScreenshotUtils.capture_dialog(dlg, width=790, height=700)
    im.save((dest_path / "vectortilelayerpropertiesinformation.png").as_posix())

    dlg.setCurrentPage("mOptsPage_Source")
    im = ScreenshotUtils.capture_dialog(dlg, width=790, height=700)
    im.save((dest_path / "vectortilelayerpropertiessource.png").as_posix())

    return {
        "vectortilelayerpropertiesinformation.png": "QgsVectorTileLayerProperties showing the 'Information' page",
        "vectortilelayerpropertiessource.png": "QgsVectorTileLayerProperties showing the 'Source' page",
    }
