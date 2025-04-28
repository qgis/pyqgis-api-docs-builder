from pathlib import Path

from qgis.core import (
    QgsNullSymbolRenderer,
    QgsStyle,
    QgsVectorLayer,
)
from qgis.gui import QgsNullSymbolRendererWidget, QgsRendererPropertiesDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):

    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    renderer = QgsNullSymbolRenderer()

    # necessary to avoid crash on some QGIS versions!
    dlg = QgsRendererPropertiesDialog(layer, QgsStyle.defaultStyle())  # noqa

    widget = QgsNullSymbolRendererWidget(layer, QgsStyle.defaultStyle(), renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "nullsymbolrendererwidget.png").as_posix())

    return {"nullsymbolrendererwidget.png": "QgsNullSymbolRendererWidget"}
