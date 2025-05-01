from pathlib import Path

from qgis.core import QgsPercentageNumericFormat
from qgis.gui import QgsPercentageNumericFormatWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsPercentageNumericFormat()
    widget = QgsPercentageNumericFormatWidget(format)

    im = ScreenshotUtils.capture_widget(widget, width=390, padding=0)
    im.save((dest_path / "percentagenumericformatwidget.png").as_posix())

    return {"percentagenumericformatwidget.png": "QgsPercentageNumericFormatWidget"}
