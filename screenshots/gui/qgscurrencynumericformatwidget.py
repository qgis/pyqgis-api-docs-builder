from pathlib import Path

from qgis.core import QgsCurrencyNumericFormat
from qgis.gui import QgsCurrencyNumericFormatWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsCurrencyNumericFormat()
    widget = QgsCurrencyNumericFormatWidget(format)

    im = ScreenshotUtils.capture_widget(widget, width=390, padding=0)
    im.save((dest_path / "currencynumericformatwidget.png").as_posix())

    return {"currencynumericformatwidget.png": "QgsCurrencyNumericFormatWidget"}
