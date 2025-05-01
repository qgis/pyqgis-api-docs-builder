from pathlib import Path

from qgis.core import QgsBasicNumericFormat
from qgis.gui import QgsNumericFormatSelectorDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsBasicNumericFormat()
    dlg = QgsNumericFormatSelectorDialog()
    dlg.setFormat(format)

    im = ScreenshotUtils.capture_dialog(dlg, width=390, height=450)
    im.save((dest_path / "numericformatselectordialog.png").as_posix())

    return {"numericformatselectordialog.png": "QgsNumericFormatSelectorDialog"}
