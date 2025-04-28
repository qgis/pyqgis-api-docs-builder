from pathlib import Path

from qgis.core import (
    QgsFillSymbol,
    QgsSingleSymbolRenderer,
    QgsStyle,
    QgsVectorLayer,
)
from qgis.gui import QgsRendererPropertiesDialog, QgsSingleSymbolRendererWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):

    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    symbol = QgsFillSymbol.createSimple({})
    symbol.setColor(QColor(120, 185, 15))
    renderer = QgsSingleSymbolRenderer(symbol)

    # necessary to avoid crash on some QGIS versions!
    dlg = QgsRendererPropertiesDialog(layer, QgsStyle.defaultStyle())  # noqa

    widget = QgsSingleSymbolRendererWidget(layer, QgsStyle.defaultStyle(), renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590, height=750)
    im.save((dest_path / "singlesymbolrendererwidget.png").as_posix())

    return {"singlesymbolrendererwidget.png": "QgsSingleSymbolRendererWidget"}
