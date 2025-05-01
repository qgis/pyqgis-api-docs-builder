from pathlib import Path

from qgis.core import QgsExpressionBasedNumericFormat
from qgis.gui import QgsExpressionBasedNumericFormatWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    format = QgsExpressionBasedNumericFormat()
    widget = QgsExpressionBasedNumericFormatWidget(format)

    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "expressionbasednumericformatwidget.png").as_posix())

    return {"expressionbasednumericformatwidget.png": "QgsExpressionBasedNumericFormatWidget"}
