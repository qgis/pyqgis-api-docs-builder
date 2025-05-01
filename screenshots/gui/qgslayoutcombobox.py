from pathlib import Path

from qgis.core import QgsPrintLayout, QgsProject
from qgis.gui import QgsLayoutComboBox

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    project = QgsProject()
    layout1 = QgsPrintLayout(project)
    layout1.setName("A3 Landscape")
    project.layoutManager().addLayout(layout1)
    layout2 = QgsPrintLayout(project)
    layout2.setName("A3 Portrait")
    project.layoutManager().addLayout(layout2)
    layout3 = QgsPrintLayout(project)
    layout3.setName("A4 Landscape")
    project.layoutManager().addLayout(layout3)

    widget = QgsLayoutComboBox(None, project.layoutManager())
    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "layoutcombobox.png").as_posix())

    im = ScreenshotUtils.capture_combo_with_dropdown(widget, width=390)
    im.save((dest_path / "layoutcomboboxexpanded.png").as_posix())

    return {
        "layoutcombobox.png": "QgsLayoutComboBox in the collapsed state",
        "layoutcomboboxexpanded.png": "QgsLayoutComboBox in the expanded state",
    }
