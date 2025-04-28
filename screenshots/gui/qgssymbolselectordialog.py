from pathlib import Path

from qgis.core import QgsFillSymbol, QgsStyle, QgsVectorLayer
from qgis.gui import QgsSymbolSelectorDialog
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    symbol = QgsFillSymbol.createSimple({})

    symbol.setColor(QColor(60, 135, 180))

    widget = QgsSymbolSelectorDialog(symbol, QgsStyle.defaultStyle(), layer)

    im = ScreenshotUtils.capture_dialog(widget, width=590, height=500)
    im.save((dest_path / "symbolselectordialog.png").as_posix())

    return {"symbolselectordialog.png": "QgsSymbolSelectorDialog"}
