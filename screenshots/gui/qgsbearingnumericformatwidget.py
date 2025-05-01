from pathlib import Path

from qgis.core import QgsBearingNumericFormat
from qgis.gui import QgsBearingNumericFormatWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsBearingNumericFormat()
    widget = QgsBearingNumericFormatWidget(format)

    im = ScreenshotUtils.capture_widget(widget, width=390, padding=0)
    im.save((dest_path / "bearingnumericformatwidget.png").as_posix())

    return {"bearingnumericformatwidget.png": "QgsBearingNumericFormatWidget"}
