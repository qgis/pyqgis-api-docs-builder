from pathlib import Path

from qgis.core import QgsFractionNumericFormat
from qgis.gui import QgsFractionNumericFormatWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsFractionNumericFormat()
    widget = QgsFractionNumericFormatWidget(format)

    im = ScreenshotUtils.capture_widget(widget, width=390, padding=0)
    im.save((dest_path / "fractionnumericformatwidget.png").as_posix())

    return {"fractionnumericformatwidget.png": "QgsFractionNumericFormatWidget"}
