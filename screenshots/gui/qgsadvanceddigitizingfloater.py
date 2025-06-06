from pathlib import Path

from qgis.core import QgsCoordinateReferenceSystem, QgsPointXY
from qgis.gui import (
    QgsAdvancedDigitizingDockWidget,
    QgsAdvancedDigitizingFloater,
    QgsMapCanvas,
    QgsMapToolCapture,
)
from qgis.PyQt.QtWidgets import QAction

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    canvas = QgsMapCanvas()
    canvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:3857"))
    widget = QgsAdvancedDigitizingDockWidget(canvas)
    map_tool = QgsMapToolCapture(canvas, widget, QgsMapToolCapture.CaptureMode.CapturePolygon)
    canvas.setMapTool(map_tool)
    map_tool.activate()

    enable_action = widget.findChild(QAction, "mEnableAction")
    enable_action.trigger()
    widget.enable()

    widget.addPoint(QgsPointXY(1000, 2000))
    widget.addPoint(QgsPointXY(1100, 2000))
    widget.constraintX().toggleLocked()

    floater = QgsAdvancedDigitizingFloater(canvas, widget)

    im = ScreenshotUtils.capture_dialog(floater, width=490, height=220)
    im.save((dest_path / "advanceddigizitingfloater.png").as_posix())

    return {"advanceddigizitingfloater.png": "QgsAdvancedDigitizingFloater"}
