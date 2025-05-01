from pathlib import Path

from qgis.gui import QgsLayoutUnitsComboBox

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsLayoutUnitsComboBox()
    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "layoutunitscombobox.png").as_posix())

    im = ScreenshotUtils.capture_combo_with_dropdown(widget, width=390)
    im.save((dest_path / "layoutunitscomboboxexpanded.png").as_posix())

    return {
        "layoutunitscombobox.png": "QgsLayoutUnitsComboBox in the collapsed state",
        "layoutunitscomboboxexpanded.png": "QgsLayoutUnitsComboBox in the expanded state",
    }
