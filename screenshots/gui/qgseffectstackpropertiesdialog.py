from pathlib import Path

from qgis.core import QgsApplication
from qgis.gui import QgsEffectStackPropertiesDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    stack = QgsApplication.paintEffectRegistry().defaultStack()
    dlg = QgsEffectStackPropertiesDialog(stack)

    im = ScreenshotUtils.capture_dialog(dlg, width=590, height=370)
    im.save((dest_path / "effectstackpropertiesdialog.png").as_posix())

    return {"effectstackpropertiesdialog.png": "QgsEffectStackPropertiesDialog"}
