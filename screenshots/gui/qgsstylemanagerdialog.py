from pathlib import Path

from qgis.core import (
    QgsStyle,
)
from qgis.gui import QgsStyleManagerDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsStyleManagerDialog(QgsStyle.defaultStyle())

    im = ScreenshotUtils.capture_dialog(
        widget, width=790, height=600, show_max=True, show_min=True
    )
    im.save((dest_path / "stylemanagerdialog.png").as_posix())

    return {"stylemanagerdialog.png": "QgsStyleManagerDialog"}
