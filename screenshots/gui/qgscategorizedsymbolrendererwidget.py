from pathlib import Path

from qgis.core import (
    QgsCategorizedSymbolRenderer,
    QgsFillSymbol,
    QgsRendererCategory,
    QgsStyle,
    QgsVectorLayer,
)
from qgis.gui import QgsCategorizedSymbolRendererWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    symbol = QgsFillSymbol.createSimple({})

    symbol.setColor(QColor(150, 0, 0))
    cat_1 = QgsRendererCategory("P", symbol.clone(), "Protected")
    symbol.setColor(QColor(230, 160, 10))
    cat_2 = QgsRendererCategory("I", symbol.clone(), "In progress")
    symbol.setColor(QColor(50, 140, 50))
    cat_3 = QgsRendererCategory("A", symbol.clone(), "Approved")

    renderer = QgsCategorizedSymbolRenderer("classification", [cat_1, cat_2, cat_3])

    symbol.setColor(QColor(240, 185, 20))
    renderer.setSourceSymbol(symbol.clone())

    widget = QgsCategorizedSymbolRendererWidget(layer, QgsStyle.defaultStyle(), renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "categorizedrendererwidget.png").as_posix())

    return {"categorizedrendererwidget.png": "QgsCategorizedSymbolRendererWidget"}
