from pathlib import Path

from qgis.gui import QgsPenJoinStyleComboBox
from qgis.PyQt.QtCore import Qt

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    combo = QgsPenJoinStyleComboBox()
    combo.setPenJoinStyle(Qt.PenJoinStyle.RoundJoin)

    im_collapsed = ScreenshotUtils.capture_widget(combo)
    im_collapsed.save((dest_path / "qgspenjoinstylecombobox_collapsed.png").as_posix())

    im_expanded = ScreenshotUtils.capture_combo_with_dropdown(combo)
    im_expanded.save((dest_path / "qgspenjoinstylecombobox_expanded.png").as_posix())

    return {
        "qgspenjoinstylecombobox_collapsed.png": "QgsPenJoinStyleComboBox in the collapsed state",
        "qgspenjoinstylecombobox_expanded.png": "QgsPenJoinStyleComboBox in the expanded state",
    }
