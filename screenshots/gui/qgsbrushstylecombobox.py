from pathlib import Path

from qgis.gui import QgsBrushStyleComboBox
from qgis.PyQt.QtCore import Qt

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    combo = QgsBrushStyleComboBox()
    combo.setBrushStyle(Qt.SolidPattern)

    im_collapsed = ScreenshotUtils.capture_widget(combo)
    im_collapsed.save((dest_path / "qgsbrushstylecombobox_collapsed.png").as_posix())

    im_expanded = ScreenshotUtils.capture_combo_with_dropdown(combo)
    im_expanded.save((dest_path / "qgsbrushstylecombobox_expanded.png").as_posix())

    return {
        "qgsbrushstylecombobox_collapsed.png": "QgsBrushStyleComboBox in the collapsed state",
        "qgsbrushstylecombobox_expanded.png": "QgsBrushStyleComboBox in the expanded state",
    }
