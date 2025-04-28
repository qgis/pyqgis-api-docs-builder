from pathlib import Path

from qgis.core import QgsCategorizedSymbolRenderer, QgsFillSymbol, QgsRendererCategory
from qgis.gui import QgsSymbolLevelsDialog
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    symbol = QgsFillSymbol.createSimple({})

    symbol.setColor(QColor(150, 0, 0))
    symbol[0].setRenderingPass(1)
    cat_1 = QgsRendererCategory("P", symbol.clone(), "Protected")
    symbol.setColor(QColor(230, 160, 10))
    symbol[0].setRenderingPass(2)
    cat_2 = QgsRendererCategory("I", symbol.clone(), "In progress")
    symbol.setColor(QColor(50, 140, 50))
    symbol[0].setRenderingPass(3)
    cat_3 = QgsRendererCategory("A", symbol.clone(), "Approved")

    renderer = QgsCategorizedSymbolRenderer("classification", [cat_1, cat_2, cat_3])
    renderer.setUsingSymbolLevels(True)

    widget = QgsSymbolLevelsDialog(renderer, True)

    im = ScreenshotUtils.capture_dialog(widget, width=590, height=300)
    im.save((dest_path / "symbollevelsdialog.png").as_posix())

    return {"symbollevelsdialog.png": "QgsSymbolLevelsDialog"}
