from pathlib import Path

from qgis.gui import QgsEffectDrawModeComboBox

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsEffectDrawModeComboBox()

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "effectdrawmodecombobox.png").as_posix())

    im = ScreenshotUtils.capture_combo_with_dropdown(widget, width=490)
    im.save((dest_path / "effectdrawmodecomboboxexpanded.png").as_posix())

    return {
        "effectdrawmodecombobox.png": "QgsEffectDrawModeComboBox in the collapsed state",
        "effectdrawmodecomboboxexpanded.png": "QgsEffectDrawModeComboBox in the expanded state",
    }
