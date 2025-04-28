from pathlib import Path

from qgis.core import (
    QgsStyle,
)
from qgis.gui import QgsStyleGroupSelectionDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsStyleGroupSelectionDialog(QgsStyle.defaultStyle())

    im = ScreenshotUtils.capture_dialog(widget, width=590, height=300)
    im.save((dest_path / "stylegroupselectiondialog.png").as_posix())

    return {"stylegroupselectiondialog.png": "QgsStyleGroupSelectionDialog"}
