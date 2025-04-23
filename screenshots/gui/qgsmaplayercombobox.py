from pathlib import Path

from qgis.core import QgsProject, QgsRasterLayer, QgsVectorLayer
from qgis.gui import QgsMapLayerComboBox

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    layer2 = QgsVectorLayer("Line", "A line layer", "memory")
    raster = QgsRasterLayer("x", "Raster layer")

    QgsProject.instance().addMapLayers([layer, layer2, raster])

    combo = QgsMapLayerComboBox()

    im_collapsed = ScreenshotUtils.capture_widget(combo)
    im_collapsed.save((dest_path / "qgsmaplayercombobox_collapsed.png").as_posix())

    im_expanded = ScreenshotUtils.capture_combo_with_dropdown(combo)
    im_expanded.save((dest_path / "qgsmaplayercombobox_expanded.png").as_posix())

    return {
        "qgsmaplayercombobox_collapsed.png": "QgsMapLayerComboBox in the collapsed state",
        "qgsmaplayercombobox_expanded.png": "QgsMapLayerComboBox in the expanded state",
    }
