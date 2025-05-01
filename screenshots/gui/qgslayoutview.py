from pathlib import Path

from qgis.core import (
    Qgis,
    QgsLayoutItemLabel,
    QgsLayoutPoint,
    QgsPrintLayout,
    QgsProject,
)
from qgis.gui import QgsLayoutView

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    project = QgsProject()
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    label = QgsLayoutItemLabel(layout)
    label.setText("A title label")
    format = label.textFormat()
    format.setSize(30)
    label.setTextFormat(format)
    label.adjustSizeToText()
    label.attemptMove(QgsLayoutPoint(5, 5, Qgis.LayoutUnit.Millimeters))
    layout.addLayoutItem(label)

    label2 = QgsLayoutItemLabel(layout)
    label2.setText("Copyright text")
    format = label2.textFormat()
    format.setSize(15)
    label2.setTextFormat(format)
    label2.adjustSizeToText()
    label2.attemptMove(QgsLayoutPoint(240, 190, Qgis.LayoutUnit.Millimeters))
    layout.addLayoutItem(label2)

    view = QgsLayoutView()
    view.setCurrentLayout(layout)
    view.zoomFull()
    layout.setSelectedItem(label)
    im = ScreenshotUtils.capture_widget(view, width=690, height=620, padding=0)
    im.save((dest_path / "layoutview.png").as_posix())

    return {"layoutview.png": "QgsLayoutView"}
