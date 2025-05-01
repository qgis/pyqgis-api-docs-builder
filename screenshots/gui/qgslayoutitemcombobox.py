from pathlib import Path

from qgis.core import QgsLayoutItemLabel, QgsLayoutItemMap, QgsPrintLayout, QgsProject
from qgis.gui import QgsLayoutItemComboBox

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    project = QgsProject()
    layout = QgsPrintLayout(project)
    layout.setName("A3 Landscape")
    project.layoutManager().addLayout(layout)
    label1 = QgsLayoutItemLabel(layout)
    label1.setId("Title label")
    layout.addLayoutItem(label1)
    label2 = QgsLayoutItemLabel(layout)
    label2.setId("Copyright text")
    layout.addLayoutItem(label2)
    map = QgsLayoutItemMap(layout)
    map.setId("Main map")
    layout.addLayoutItem(map)

    widget = QgsLayoutItemComboBox(None, layout)
    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "layoutitemcombobox.png").as_posix())

    im = ScreenshotUtils.capture_combo_with_dropdown(widget, width=390)
    im.save((dest_path / "layoutitemcomboboxexpanded.png").as_posix())

    return {
        "layoutitemcombobox.png": "QgsLayoutItemComboBox in the collapsed state",
        "layoutitemcomboboxexpanded.png": "QgsLayoutItemComboBox in the expanded state",
    }
