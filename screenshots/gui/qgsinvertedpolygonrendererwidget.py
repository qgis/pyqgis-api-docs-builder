from pathlib import Path

from qgis.core import (
    QgsFillSymbol,
    QgsInvertedPolygonRenderer,
    QgsSingleSymbolRenderer,
    QgsStyle,
    QgsVectorLayer,
)
from qgis.gui import QgsInvertedPolygonRendererWidget, QgsRendererPropertiesDialog
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):

    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    symbol = QgsFillSymbol.createSimple({})
    symbol.setColor(QColor(120, 185, 15))
    sub_renderer = QgsSingleSymbolRenderer(symbol)

    renderer = QgsInvertedPolygonRenderer(sub_renderer)

    # necessary to avoid crash on some QGIS versions!
    dlg = QgsRendererPropertiesDialog(layer, QgsStyle.defaultStyle())  # noqa

    widget = QgsInvertedPolygonRendererWidget(layer, QgsStyle.defaultStyle(), renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "invertedpolygonrendererwidget.png").as_posix())

    return {"invertedpolygonrendererwidget.png": "QgsInvertedPolygonRendererWidget"}
