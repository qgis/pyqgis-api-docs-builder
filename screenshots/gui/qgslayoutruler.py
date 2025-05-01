from pathlib import Path

from qgis.core import QgsPrintLayout, QgsProject
from qgis.gui import QgsLayoutRuler, QgsLayoutView
from qgis.PyQt.QtCore import QPointF

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    project = QgsProject()
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    view = QgsLayoutView()
    view.setCurrentLayout(layout)
    widget = QgsLayoutRuler()
    widget.setLayoutView(view)
    widget.setCursorPosition(QPointF(223, 0))
    im = ScreenshotUtils.capture_widget(widget, width=490, padding=0)
    im.save((dest_path / "layoutruler.png").as_posix())

    return {"layoutruler.png": "QgsLayoutRuler"}
