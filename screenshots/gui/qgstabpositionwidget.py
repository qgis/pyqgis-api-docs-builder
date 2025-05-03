from pathlib import Path

from qgis.core import QgsTextFormat
from qgis.gui import QgsTabPositionWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsTabPositionWidget()
    widget.setPositions(
        [
            QgsTextFormat.Tab(80),
            QgsTextFormat.Tab(130),
            QgsTextFormat.Tab(180),
            QgsTextFormat.Tab(210),
        ]
    )

    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "tabpositionwidget.png").as_posix())

    return {"tabpositionwidget.png": "QgsTabPositionWidget"}
