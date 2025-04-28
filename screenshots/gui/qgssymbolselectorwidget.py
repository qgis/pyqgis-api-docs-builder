from pathlib import Path

from qgis.core import QgsFillSymbol, QgsStyle, QgsVectorLayer
from qgis.gui import QgsSymbolSelectorWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    symbol = QgsFillSymbol.createSimple({})

    symbol.setColor(QColor(60, 135, 180))

    widget = QgsSymbolSelectorWidget(symbol, QgsStyle.defaultStyle(), layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, height=500)
    im.save((dest_path / "symbolselectorwidget.png").as_posix())

    return {"symbolselectorwidget.png": "QgsSymbolSelectorWidget"}
