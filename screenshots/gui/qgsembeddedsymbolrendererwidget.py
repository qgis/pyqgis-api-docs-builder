from pathlib import Path

from qgis.core import QgsEmbeddedSymbolRenderer, QgsMarkerSymbol, QgsVectorLayer
from qgis.gui import QgsEmbeddedSymbolRendererWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer(
        (Path(__file__).parent / ".." / "resources" / "samples.kml").as_posix(),
        "A point layer",
        "ogr",
    )
    default_symbol = QgsMarkerSymbol.createSimple({})
    renderer = QgsEmbeddedSymbolRenderer(default_symbol)
    widget = QgsEmbeddedSymbolRendererWidget(layer, None, renderer)

    im = ScreenshotUtils.capture_widget(widget, width=590, height=100)
    im.save((dest_path / "embeddedsymbolrendererwidget.png").as_posix())

    layer = QgsVectorLayer("Point", "My sample layer", "memory")
    default_symbol = QgsMarkerSymbol.createSimple({})
    renderer = QgsEmbeddedSymbolRenderer(default_symbol)
    widget = QgsEmbeddedSymbolRendererWidget(layer, None, renderer)
    im = ScreenshotUtils.capture_widget(widget, width=590, height=100, padding=0)
    im.save((dest_path / "embeddedsymbolrendererwidgetnotembedded.png").as_posix())

    return {
        "embeddedsymbolrendererwidget.png": "QgsEmbeddedSymbolRendererWidget for a layer containing embedded symbols",
        "embeddedsymbolrendererwidgetnotembedded.png": "QgsEmbeddedSymbolRendererWidget for a layer without embedded symbols",
    }
