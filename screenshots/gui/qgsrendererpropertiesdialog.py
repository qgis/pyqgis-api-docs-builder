from pathlib import Path

from qgis.core import QgsMarkerSymbol, QgsSingleSymbolRenderer, QgsStyle, QgsVectorLayer
from qgis.gui import QgsRendererPropertiesDialog
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "Point Layer", "memory")
    symbol = QgsMarkerSymbol.createSimple({})
    symbol.setColor(QColor(120, 185, 15))
    layer.setRenderer(QgsSingleSymbolRenderer(symbol))
    widget = QgsRendererPropertiesDialog(layer, QgsStyle.defaultStyle())

    im = ScreenshotUtils.capture_dialog(widget, width=590)
    im.save((dest_path / "rendererpropertiesdialog.png").as_posix())

    widget = QgsRendererPropertiesDialog(layer, QgsStyle.defaultStyle(), embedded=True)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "rendererpropertiesdialogembedded.png").as_posix())

    return {
        "rendererpropertiesdialog.png": "QgsRendererPropertiesDialog showing a QgsSingleSymbolRenderer in the default (dialog) mode",
        "rendererpropertiesdialogembedded.png": "QgsRendererPropertiesDialog showing a QgsSingleSymbolRenderer in an embedded widget mode",
    }
