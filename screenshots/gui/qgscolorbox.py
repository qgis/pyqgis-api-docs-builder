from pathlib import Path

from qgis.gui import QgsColorBox, QgsColorWidget
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsColorBox()
    widget.setColor(QColor(100, 150, 200))

    im = ScreenshotUtils.capture_widget(widget, width=320, height=320)
    im.save((dest_path / "color_box_value.png").as_posix())

    widget.setComponent(QgsColorWidget.ColorComponent.Hue)
    widget.setColor(QColor(150, 150, 200))
    im = ScreenshotUtils.capture_widget(widget, width=320, height=320)
    im.save((dest_path / "color_box_hue.png").as_posix())

    return {
        "color_box_value.png": "QgsColorBox using the QgsColorWidget.ColorComponent.Value component",
        "color_box_hue.png": "QgsColorBox using the QgsColorWidget.ColorComponent.Hue component",
    }
