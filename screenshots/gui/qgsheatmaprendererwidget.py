from pathlib import Path

from qgis.core import (
    QgsHeatmapRenderer,
    QgsStyle,
    QgsVectorLayer,
)
from qgis.gui import QgsHeatmapRendererWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")

    renderer = QgsHeatmapRenderer()
    widget = QgsHeatmapRendererWidget(layer, QgsStyle.defaultStyle(), renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "heatmaprendererwidget.png").as_posix())

    return {"heatmaprendererwidget.png": "QgsHeatmapRendererWidget"}
