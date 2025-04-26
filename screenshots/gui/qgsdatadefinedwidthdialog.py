from pathlib import Path

from qgis.core import QgsLineSymbol, QgsProperty, QgsVectorLayer
from qgis.gui import QgsDataDefinedWidthDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("LineString", "A line layer", "memory")
    symbol = QgsLineSymbol.createSimple({})
    symbol.setWidth(1)
    symbol.setDataDefinedWidth(QgsProperty.fromExpression("1+2"))

    widget = QgsDataDefinedWidthDialog([symbol], layer)
    widget.setWindowTitle("Data Defined Width")

    im = ScreenshotUtils.capture_dialog(widget, width=350)
    im.save((dest_path / "datadefinedwidthdialog.png").as_posix())

    return {
        "datadefinedwidthdialog.png": "QgsDataDefinedWidthDialog with data-defined width enabled"
    }
