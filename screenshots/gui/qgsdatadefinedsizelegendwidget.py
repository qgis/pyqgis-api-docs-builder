from pathlib import Path

from qgis.core import (
    QgsDataDefinedSizeLegend,
    QgsMarkerSymbol,
    QgsProperty,
    QgsSizeScaleTransformer,
)
from qgis.gui import QgsDataDefinedSizeLegendWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    symbol = QgsMarkerSymbol.createSimple({})
    symbol.setSize(3)
    symbol.setDataDefinedSize(QgsProperty.fromExpression("1+2"))

    legend = QgsDataDefinedSizeLegend()
    legend.setSymbol(symbol.clone())
    legend.setLegendType(QgsDataDefinedSizeLegend.LegendType.LegendCollapsed)
    legend.setTitle("My Legend")
    legend.setSizeScaleTransformer(QgsSizeScaleTransformer())
    legend.setClasses(
        [
            QgsDataDefinedSizeLegend.SizeClass(3, "Small"),
            QgsDataDefinedSizeLegend.SizeClass(6, "Medium"),
            QgsDataDefinedSizeLegend.SizeClass(10, "Large"),
        ]
    )
    widget = QgsDataDefinedSizeLegendWidget(
        legend, QgsProperty.fromExpression('"my_field" * 2'), symbol
    )

    im = ScreenshotUtils.capture_widget(widget, width=550, height=700, padding=0)
    im.save((dest_path / "datadefinedsizelegendwidget.png").as_posix())

    return {
        "datadefinedsizelegendwidget.png": "QgsDataDefinedSizeLegendWidget allowing customization of data-defined size legends"
    }
