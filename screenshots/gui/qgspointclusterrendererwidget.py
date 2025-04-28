from pathlib import Path

from qgis.core import (
    QgsMarkerSymbol,
    QgsPointClusterRenderer,
    QgsSingleSymbolRenderer,
    QgsStyle,
    QgsVectorLayer,
)
from qgis.gui import QgsPointClusterRendererWidget, QgsRendererPropertiesDialog
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):

    layer = QgsVectorLayer("Point", "A point layer", "memory")
    symbol = QgsMarkerSymbol.createSimple({})
    symbol.setColor(QColor(120, 185, 15))
    sub_renderer = QgsSingleSymbolRenderer(symbol)

    renderer = QgsPointClusterRenderer()
    renderer.setEmbeddedRenderer(sub_renderer)

    # necessary to avoid crash on some QGIS versions!
    dlg = QgsRendererPropertiesDialog(layer, QgsStyle.defaultStyle())  # noqa

    widget = QgsPointClusterRendererWidget(layer, QgsStyle.defaultStyle(), renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "pointclusterrendererwidget.png").as_posix())

    return {"pointclusterrendererwidget.png": "QgsPointClusterRendererWidget"}
