from pathlib import Path

from qgis.core import QgsFillSymbol, QgsStyle, QgsVectorLayer
from qgis.gui import QgsSymbolsListWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    symbol = QgsFillSymbol.createSimple({})

    symbol.setColor(QColor(60, 135, 180))

    widget = QgsSymbolsListWidget(
        symbol, QgsStyle.defaultStyle(), menu=None, parent=None, layer=layer
    )

    im = ScreenshotUtils.capture_widget(widget, width=590, height=500)
    im.save((dest_path / "symbolslistwidget.png").as_posix())

    return {"symbolslistwidget.png": "QgsSymbolsListWidget"}
