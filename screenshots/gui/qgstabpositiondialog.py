from pathlib import Path

from qgis.core import QgsTextFormat
from qgis.gui import QgsTabPositionDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    dlg = QgsTabPositionDialog()
    dlg.setPositions(
        [
            QgsTextFormat.Tab(80),
            QgsTextFormat.Tab(130),
            QgsTextFormat.Tab(180),
            QgsTextFormat.Tab(210),
        ]
    )

    im = ScreenshotUtils.capture_dialog(dlg, width=390, height=300)
    im.save((dest_path / "tabpositiondialog.png").as_posix())

    return {"tabpositiondialog.png": "QgsTabPositionDialog"}
