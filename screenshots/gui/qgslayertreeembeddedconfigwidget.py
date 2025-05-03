from pathlib import Path

from qgis.core import QgsVectorLayer
from qgis.gui import QgsLayerTreeEmbeddedConfigWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("LineString", "Lines", "memory")

    widget = QgsLayerTreeEmbeddedConfigWidget()
    widget.setLayer(layer)

    im = ScreenshotUtils.capture_widget(widget, width=390, height=250, padding=0)
    im.save((dest_path / "layertreeembeddedconfigwidget.png").as_posix())

    return {"layertreeembeddedconfigwidget.png": "QgsLayerTreeEmbeddedConfigWidget"}
