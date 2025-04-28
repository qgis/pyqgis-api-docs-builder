from pathlib import Path

from qgis.core import QgsMarkerSymbol, QgsRuleBasedRenderer, QgsStyle, QgsVectorLayer
from qgis.gui import QgsRendererRulePropsWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "Point Layer", "memory")
    symbol = QgsMarkerSymbol.createSimple({})
    symbol.setColor(QColor(120, 185, 15))
    root_rule = QgsRuleBasedRenderer.Rule(None)
    child_rule = QgsRuleBasedRenderer.Rule(
        symbol,
        filterExp='"category"=4',
        label="Protected species",
        description="Category matching protected species",
    )
    root_rule.appendChild(child_rule)

    layer.setRenderer(QgsRuleBasedRenderer(root_rule))
    widget = QgsRendererRulePropsWidget(child_rule, layer, QgsStyle.defaultStyle())

    im = ScreenshotUtils.capture_widget(widget, width=590, height=650)
    im.save((dest_path / "rendererrulepropswidget.png").as_posix())

    return {"rendererrulepropswidget.png": "QgsRendererRulePropsWidget"}
