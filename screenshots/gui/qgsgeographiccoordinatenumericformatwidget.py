from pathlib import Path

from qgis.core import QgsGeographicCoordinateNumericFormat
from qgis.gui import QgsGeographicCoordinateNumericFormatWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsGeographicCoordinateNumericFormat()
    widget = QgsGeographicCoordinateNumericFormatWidget(format)

    im = ScreenshotUtils.capture_widget(widget, width=390, padding=0)
    im.save((dest_path / "geographiccoordinatenumericformatwidget.png").as_posix())

    return {
        "geographiccoordinatenumericformatwidget.png": "QgsGeographicCoordinateNumericFormatWidget"
    }
