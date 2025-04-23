from pathlib import Path

from qgis.gui import QgsColorButton
from qgis.PyQt.QtGui import QColor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsColorButton()
    widget.setColor(QColor(100, 150, 200))
    widget.setFixedWidth(180)

    im = ScreenshotUtils.capture_widget(widget, width=200)
    im.save((dest_path / "color_button.png").as_posix())

    # triggers a crash in qgis!
    # im = ScreenshotUtils.capture_toolbutton_with_dropdown(widget, width=250)
    # im.save((dest_path / "color_button_expanded.png").as_posix())

    return {
        "color_button.png": "QgsColorButton in a default state",
        "color_button_expanded.png": "QgsColorButton showing drop down menu",
    }
