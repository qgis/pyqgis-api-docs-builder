from pathlib import Path

from qgis.core import QgsBasicNumericFormat
from qgis.gui import QgsBasicNumericFormatWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsBasicNumericFormat()
    widget = QgsBasicNumericFormatWidget(format)

    im = ScreenshotUtils.capture_widget(widget, width=390, padding=0)
    im.save((dest_path / "basicnumericformat.png").as_posix())

    return {"basicnumericformat.png": "QgsBasicNumericFormatWidget"}
