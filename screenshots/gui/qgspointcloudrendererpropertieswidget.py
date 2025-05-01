from pathlib import Path

from qgis.core import QgsPointCloudLayer, QgsStyle
from qgis.gui import QgsPointCloudRendererPropertiesWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (
        Path(__file__).parent / ".." / "resources" / "point_cloud" / "ept.json"
    ).as_posix()
    layer = QgsPointCloudLayer(layer_path, "Point Cloud", "ept")

    widget = QgsPointCloudRendererPropertiesWidget(layer, QgsStyle.defaultStyle())

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "pointcloudrendererpropertieswidget.png").as_posix())

    return {"pointcloudrendererpropertieswidget.png": "QgsPointCloudRendererPropertiesWidget"}
