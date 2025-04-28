from pathlib import Path

from qgis.gui import QgsPenStyleComboBox
from qgis.PyQt.QtCore import Qt

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    combo = QgsPenStyleComboBox()
    combo.setPenStyle(Qt.PenStyle.DashLine)

    im_collapsed = ScreenshotUtils.capture_widget(combo)
    im_collapsed.save((dest_path / "qgspenstylecombobox_collapsed.png").as_posix())

    im_expanded = ScreenshotUtils.capture_combo_with_dropdown(combo)
    im_expanded.save((dest_path / "qgspenstylecombobox_expanded.png").as_posix())

    return {
        "qgspenstylecombobox_collapsed.png": "QgsPenStyleComboBox in the collapsed state",
        "qgspenstylecombobox_expanded.png": "QgsPenStyleComboBox in the expanded state",
    }
