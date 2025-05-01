from pathlib import Path

from qgis.core import QgsRasterLayer
from qgis.gui import QgsRasterBandComboBox

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "landsat.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")
    widget = QgsRasterBandComboBox()
    widget.setLayer(layer)
    widget.setBand(1)

    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "rasterbandcombobox.png").as_posix())

    im = ScreenshotUtils.capture_combo_with_dropdown(widget, width=390)
    im.save((dest_path / "rasterbandcomboboxexpanded.png").as_posix())

    return {
        "rasterbandcombobox.png": "QgsRasterBandComboBox in the collapsed state",
        "rasterbandcomboboxexpanded.png": "QgsRasterBandComboBox in the expanded state",
    }
