from pathlib import Path

from qgis.core import QgsBearingNumericFormat
from qgis.gui import QgsBearingNumericFormatDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsBearingNumericFormat()
    dialog = QgsBearingNumericFormatDialog(format)

    im = ScreenshotUtils.capture_dialog(dialog, width=390, height=200)
    im.save((dest_path / "bearingnumericformatdialog.png").as_posix())

    return {"bearingnumericformatdialog.png": "QgsBearingNumericFormatDialog"}
