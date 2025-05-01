from pathlib import Path

from qgis.core import (
    QgsColorRampShader,
    QgsGradientColorRamp,
)
from qgis.gui import QgsColorRampShaderWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    ramp = QgsGradientColorRamp()
    shader = QgsColorRampShader(0, 1000, ramp)
    shader.setColorRampItemList(
        [
            QgsColorRampShader.ColorRampItem(0, ramp.color(0)),
            QgsColorRampShader.ColorRampItem(250, ramp.color(0.25)),
            QgsColorRampShader.ColorRampItem(500, ramp.color(0.5)),
            QgsColorRampShader.ColorRampItem(750, ramp.color(0.75)),
            QgsColorRampShader.ColorRampItem(1000, ramp.color(1.0)),
        ]
    )
    widget = QgsColorRampShaderWidget()
    widget.setFromShader(shader)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "colorrampshaderwidget.png").as_posix())

    return {"colorrampshaderwidget.png": "QgsColorRampShaderWidget"}
