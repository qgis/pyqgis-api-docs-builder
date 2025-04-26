from pathlib import Path

from qgis.core import QgsMarkerSymbol, QgsProperty, QgsVectorLayer
from qgis.gui import QgsDataDefinedSizeDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    symbol = QgsMarkerSymbol.createSimple({})
    symbol.setSize(3)
    symbol.setDataDefinedSize(QgsProperty.fromExpression("1+2"))

    widget = QgsDataDefinedSizeDialog([symbol], layer)
    widget.setWindowTitle("Data Defined Size")

    im = ScreenshotUtils.capture_dialog(widget, width=350)
    im.save((dest_path / "datadefinedsizedialog.png").as_posix())

    return {"datadefinedsizedialog.png": "QgsDataDefinedSizeDialog with data-defined size enabled"}
