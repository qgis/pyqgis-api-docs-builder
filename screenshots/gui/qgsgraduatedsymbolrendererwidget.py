from pathlib import Path

from qgis.core import (
    Qgis,
    QgsFillSymbol,
    QgsGraduatedSymbolRenderer,
    QgsMarkerSymbol,
    QgsRendererRange,
    QgsStyle,
    QgsVectorLayer,
)
from qgis.gui import QgsGraduatedSymbolRendererWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    # color varying
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    symbol = QgsFillSymbol.createSimple({})

    symbol.setColor(QColor(150, 0, 0))
    range_1 = QgsRendererRange(0, 10, symbol.clone(), "Low")
    symbol.setColor(QColor(230, 160, 10))
    range_2 = QgsRendererRange(10, 50, symbol.clone(), "Medium")
    symbol.setColor(QColor(50, 140, 50))
    range_3 = QgsRendererRange(50, 100, symbol.clone(), "High")

    renderer = QgsGraduatedSymbolRenderer("quantity", [range_1, range_2, range_3])

    symbol.setColor(QColor(240, 185, 20))
    renderer.setSourceSymbol(symbol.clone())

    widget = QgsGraduatedSymbolRendererWidget(layer, QgsStyle.defaultStyle(), renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "graduatedrendererwidgetbycolor.png").as_posix())

    # size varying
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    symbol = QgsMarkerSymbol.createSimple({})

    symbol.setColor(QColor(15, 130, 180))
    symbol.setSize(1)
    range_1 = QgsRendererRange(0, 10, symbol.clone(), "Low")
    symbol.setSize(2)
    range_2 = QgsRendererRange(10, 50, symbol.clone(), "Medium")
    symbol.setSize(3)
    range_3 = QgsRendererRange(50, 100, symbol.clone(), "High")

    renderer = QgsGraduatedSymbolRenderer("quantity", [range_1, range_2, range_3])
    renderer.setGraduatedMethod(Qgis.GraduatedMethod.Size)

    symbol.setSize(1)
    renderer.setSourceSymbol(symbol.clone())

    widget = QgsGraduatedSymbolRendererWidget(layer, QgsStyle.defaultStyle(), renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "graduatedrendererwidgetbysize.png").as_posix())

    return {
        "graduatedrendererwidgetbycolor.png": "QgsGraduatedSymbolRenderer for a color varying symbol",
        "graduatedrendererwidgetbysize.png": "QgsGraduatedSymbolRenderer for a size varying symbol",
    }
