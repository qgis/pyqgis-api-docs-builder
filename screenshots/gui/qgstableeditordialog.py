from pathlib import Path

from qgis.core import QgsTableCell, QgsTextFormat
from qgis.gui import QgsTableEditorDialog
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    dlg = QgsTableEditorDialog()
    header = QgsTableCell("My table")
    header.setSpan(1, 2)
    header.setHorizontalAlignment(Qt.AlignHCenter)
    header.setBackgroundColor(QColor(240, 245, 230))
    text_format = QgsTextFormat()
    text_format.setColor(QColor(0, 0, 80))
    header.setTextFormat(text_format)
    dlg.setTableContents(
        [
            [header, QgsTableCell()],
            [QgsTableCell("First cell"), QgsTableCell("Second cell")],
            [QgsTableCell(55), QgsTableCell(110)],
        ]
    )
    dlg.setTableColumnWidth(0, 100)
    dlg.setTableColumnWidth(1, 80)
    dock = dlg.findChild(QWidget, "FormattingDock")
    dock.setFixedWidth(400)

    im = ScreenshotUtils.capture_dialog(dlg, width=690, height=500, show_max=True, show_min=True)
    im.save((dest_path / "tableeditordialog.png").as_posix())

    return {"tableeditordialog.png": "QgsTableEditorDialog"}
