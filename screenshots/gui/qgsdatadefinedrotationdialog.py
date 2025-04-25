from pathlib import Path

from qgis.core import QgsMarkerSymbol, QgsProperty, QgsVectorLayer
from qgis.gui import QgsDataDefinedRotationDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "A point layer", "memory")
    symbol = QgsMarkerSymbol.createSimple({})
    symbol.setAngle(45)
    symbol.setDataDefinedAngle(QgsProperty.fromExpression("1+2"))

    widget = QgsDataDefinedRotationDialog([symbol], layer)
    widget.setWindowTitle("Data Defined Rotation")

    im = ScreenshotUtils.capture_dialog(widget, width=350, height=150)
    im.save((dest_path / "datadefinedrotationdialog.png").as_posix())

    return {
        "datadefinedrotationdialog.png": "QgsDataDefinedRotationDialog with data-defined rotation enabled"
    }
