from pathlib import Path

from qgis.core import Qgs25DRenderer, QgsStyle, QgsVectorLayer
from qgis.gui import Qgs25DRendererWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Polygon", "A polygon layer", "memory")
    renderer = Qgs25DRenderer()
    widget = Qgs25DRendererWidget(layer, QgsStyle.defaultStyle(), renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590, height=820)
    im.save((dest_path / "25drendererwidget.png").as_posix())

    return {"25drendererwidget.png": "Qgs25DRendererWidget showing default Qgs25DRenderer state"}
