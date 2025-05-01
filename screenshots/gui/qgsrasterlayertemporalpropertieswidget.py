from pathlib import Path

from qgis.core import QgsDateTimeRange, QgsRasterLayer
from qgis.gui import QgsRasterLayerTemporalPropertiesWidget
from qgis.PyQt.QtCore import QDateTime

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "dem.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")
    layer.temporalProperties().setIsActive(True)
    layer.temporalProperties().setFixedTemporalRange(
        QgsDateTimeRange(QDateTime(2020, 6, 1, 0, 0, 0), QDateTime(2020, 7, 1, 23, 59, 59))
    )

    widget = QgsRasterLayerTemporalPropertiesWidget(None, layer)

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "rasterlayertemporalpropertieswidget.png").as_posix())

    return {"rasterlayertemporalpropertieswidget.png": "QgsRasterLayerTemporalPropertiesWidget"}
