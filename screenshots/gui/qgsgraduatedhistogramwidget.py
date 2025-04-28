import random
from pathlib import Path

from qgis.core import (
    QgsFeature,
    QgsFillSymbol,
    QgsGraduatedSymbolRenderer,
    QgsRendererRange,
    QgsVectorLayer,
)
from qgis.gui import QgsGraduatedHistogramWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    # populate layer with a good number of sample values, roughly normally distributed
    random.seed(42)
    layer = QgsVectorLayer("Polygon?field=quantity:real", "A polygon layer", "memory")
    values = [random.gauss(50, 15) for _ in range(1000)]
    values = [max(0, min(100, value)) for value in values]
    for v in values:
        f = QgsFeature(layer.fields())
        f["quantity"] = v
        layer.dataProvider().addFeature(f)

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

    widget = QgsGraduatedHistogramWidget()
    widget.setRenderer(renderer)
    widget.setGraduatedRanges(renderer.ranges())
    widget.setSourceFieldExp(renderer.classAttribute())
    widget.setLayer(layer)
    widget.refreshValues()

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "graduatedhistogramwidget.png").as_posix())

    return {
        "graduatedhistogramwidget.png": "QgsGraduatedHistogramWidget showing a normally distributed histogram"
    }
