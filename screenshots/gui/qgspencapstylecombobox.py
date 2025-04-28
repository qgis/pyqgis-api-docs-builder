from pathlib import Path

from qgis.gui import QgsPenCapStyleComboBox
from qgis.PyQt.QtCore import Qt

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    combo = QgsPenCapStyleComboBox()
    combo.setPenCapStyle(Qt.PenCapStyle.FlatCap)

    im_collapsed = ScreenshotUtils.capture_widget(combo)
    im_collapsed.save((dest_path / "qgspencapstylecombobox_collapsed.png").as_posix())

    im_expanded = ScreenshotUtils.capture_combo_with_dropdown(combo)
    im_expanded.save((dest_path / "qgspencapstylecombobox_expanded.png").as_posix())

    return {
        "qgspencapstylecombobox_collapsed.png": "QgsPenCapStyleComboBox in the collapsed state",
        "qgspencapstylecombobox_expanded.png": "QgsPenCapStyleComboBox in the expanded state",
    }
