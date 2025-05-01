from pathlib import Path

from qgis.core import QgsGeographicCoordinateNumericFormat
from qgis.gui import QgsGeographicCoordinateNumericFormatDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsGeographicCoordinateNumericFormat()
    dlg = QgsGeographicCoordinateNumericFormatDialog(format)

    im = ScreenshotUtils.capture_dialog(dlg, width=390, height=250)
    im.save((dest_path / "geographiccoordinatenumericformatdialog.png").as_posix())

    return {
        "geographiccoordinatenumericformatdialog.png": "QgsGeographicCoordinateNumericFormatDialog"
    }
