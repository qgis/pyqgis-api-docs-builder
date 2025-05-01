from pathlib import Path

from qgis.core import QgsPalettedRasterRenderer, QgsRasterLayer
from qgis.gui import QgsPalettedRendererWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "landsat.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")
    renderer = QgsPalettedRasterRenderer(
        layer.dataProvider(),
        1,
        [
            QgsPalettedRasterRenderer.Class(1, QColor(200, 0, 0)),
            QgsPalettedRasterRenderer.Class(2, QColor(0, 200, 0)),
        ],
    )

    layer.setRenderer(renderer)
    widget = QgsPalettedRendererWidget(layer)

    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "palettedrendererwidget.png").as_posix())

    return {"palettedrendererwidget.png": "QgsPalettedRendererWidget"}
