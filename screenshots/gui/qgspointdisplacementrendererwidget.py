from pathlib import Path

from qgis.core import (
    QgsMarkerSymbol,
    QgsPointDisplacementRenderer,
    QgsSingleSymbolRenderer,
    QgsStyle,
    QgsVectorLayer,
)
from qgis.gui import QgsPointDisplacementRendererWidget, QgsRendererPropertiesDialog
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):

    layer = QgsVectorLayer("Point", "A point layer", "memory")
    symbol = QgsMarkerSymbol.createSimple({})
    symbol.setColor(QColor(120, 185, 15))
    sub_renderer = QgsSingleSymbolRenderer(symbol)

    renderer = QgsPointDisplacementRenderer()
    renderer.setEmbeddedRenderer(sub_renderer)

    # necessary to avoid crash on some QGIS versions!
    dlg = QgsRendererPropertiesDialog(layer, QgsStyle.defaultStyle())  # noqa

    widget = QgsPointDisplacementRendererWidget(layer, QgsStyle.defaultStyle(), renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "pointdisplacementrendererwidget.png").as_posix())

    return {"pointdisplacementrendererwidget.png": "QgsPointDisplacementRendererWidget"}
