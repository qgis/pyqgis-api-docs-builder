from pathlib import Path

from qgis.core import QgsBasicNumericFormat
from qgis.gui import QgsNumericFormatSelectorWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsBasicNumericFormat()
    widget = QgsNumericFormatSelectorWidget()
    widget.setFormat(format)

    im = ScreenshotUtils.capture_widget(widget, width=390, padding=0)
    im.save((dest_path / "numericformatselectorwidget.png").as_posix())

    return {"numericformatselectorwidget.png": "QgsNumericFormatSelectorWidget"}
