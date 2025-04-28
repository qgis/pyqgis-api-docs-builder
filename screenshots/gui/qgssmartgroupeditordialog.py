from pathlib import Path

from qgis.core import (
    QgsStyle,
)
from qgis.gui import QgsSmartGroupEditorDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsSmartGroupEditorDialog(QgsStyle.defaultStyle())
    widget.setSmartgroupName("My Group")
    widget.addCondition()

    im = ScreenshotUtils.capture_dialog(widget, width=590, height=300)
    im.save((dest_path / "smartgroupeditordialog.png").as_posix())

    return {"smartgroupeditordialog.png": "QgsSmartGroupEditorDialog"}
