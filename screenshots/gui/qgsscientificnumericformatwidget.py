from pathlib import Path

from qgis.core import QgsScientificNumericFormat
from qgis.gui import QgsScientificNumericFormatWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsScientificNumericFormat()
    widget = QgsScientificNumericFormatWidget(format)

    im = ScreenshotUtils.capture_widget(widget, width=390, padding=0)
    im.save((dest_path / "scientificnumericformatwidget.png").as_posix())

    return {"scientificnumericformatwidget.png": "QgsScientificNumericFormatWidget"}
