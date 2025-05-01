from pathlib import Path

from qgis.core import Qgis, QgsLayoutPoint, QgsLayoutSize, QgsPrintLayout, QgsProject
from qgis.gui import QgsLayoutItemPropertiesDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    project = QgsProject()
    layout = QgsPrintLayout(project)
    widget = QgsLayoutItemPropertiesDialog()
    widget.setLayout(layout)
    widget.setItemSize(QgsLayoutSize(15, 10, Qgis.LayoutUnit.Centimeters))
    widget.setItemPosition(QgsLayoutPoint(5, 7.5, Qgis.LayoutUnit.Centimeters))
    im = ScreenshotUtils.capture_dialog(widget, width=490)
    im.save((dest_path / "layoutitempropertiesdialog.png").as_posix())

    return {"layoutitempropertiesdialog.png": "QgsLayoutItemPropertiesDialog"}
