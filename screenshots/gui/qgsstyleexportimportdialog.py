from pathlib import Path

from qgis.core import (
    QgsStyle,
)
from qgis.gui import QgsStyleExportImportDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsStyleExportImportDialog(
        QgsStyle.defaultStyle(), mode=QgsStyleExportImportDialog.Mode.Export
    )

    im = ScreenshotUtils.capture_dialog(widget, width=590, height=300)
    im.save((dest_path / "styleexportimportdialogexport.png").as_posix())

    widget = QgsStyleExportImportDialog(
        QgsStyle.defaultStyle(), mode=QgsStyleExportImportDialog.Mode.Import
    )
    widget.setImportFilePath("c:\\QGIS Data\\My Style.xml")

    im = ScreenshotUtils.capture_dialog(widget, width=590, height=300)
    im.save((dest_path / "styleexportimportdialogimport.png").as_posix())

    return {
        "styleexportimportdialogexport.png": "QgsStyleExportImportDialog showing the export mode",
        "styleexportimportdialogimport.png": "QgsStyleExportImportDialog showing the import mode",
    }
