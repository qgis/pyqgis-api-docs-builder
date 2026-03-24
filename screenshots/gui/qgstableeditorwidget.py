from pathlib import Path

from qgis.core import QgsTableCell, QgsTextFormat
from qgis.gui import QgsTableEditorWidget
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsTableEditorWidget()
    header = QgsTableCell("My table")
    header.setSpan(1, 2)
    header.setHorizontalAlignment(Qt.AlignmentFlag.AlignHCenter)
    header.setBackgroundColor(QColor(240, 245, 230))
    text_format = QgsTextFormat()
    text_format.setColor(QColor(0, 0, 80))
    header.setTextFormat(text_format)
    widget.setTableContents(
        [
            [header, QgsTableCell()],
            [QgsTableCell("First cell"), QgsTableCell("Second cell")],
            [QgsTableCell(55), QgsTableCell(110)],
        ]
    )
    widget.setTableColumnWidth(0, 100)
    widget.setTableColumnWidth(1, 80)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=300, padding=0)
    im.save((dest_path / "tableeditorwidget.png").as_posix())

    return {"tableeditorwidget.png": "QgsTableEditorWidget"}
