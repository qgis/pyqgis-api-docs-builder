from pathlib import Path

from qgis.core import (
    QgsColorRampShader,
    QgsGradientColorRamp,
    QgsInterpolatedLineColor,
    QgsInterpolatedLineSymbolLayer,
    QgsInterpolatedLineWidth,
    QgsProperty,
    QgsSymbolLayer,
    QgsVectorLayer,
)
from qgis.gui import QgsInterpolatedLineSymbolLayerWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("LineString", "A line layer", "memory")
    widget = QgsInterpolatedLineSymbolLayerWidget(layer)

    symbol_layer = QgsInterpolatedLineSymbolLayer()
    interpolated_width = QgsInterpolatedLineWidth()
    interpolated_width.setMinimumWidth(0.2)
    interpolated_width.setMaximumWidth(1)
    interpolated_width.setMinimumValue(0)
    interpolated_width.setMaximumValue(1000)
    interpolated_width.setIsVariableWidth(True)
    symbol_layer.setInterpolatedWidth(interpolated_width)
    symbol_layer.setDataDefinedProperty(
        QgsSymbolLayer.PropertyLineStartWidthValue, QgsProperty.fromField("measure_at_start")
    )
    symbol_layer.setDataDefinedProperty(
        QgsSymbolLayer.PropertyLineEndWidthValue, QgsProperty.fromField("measure_at_end")
    )
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "interpolatedlinesymbollayerwidgetvariablelinewidth.png").as_posix())

    interpolated_width.setIsVariableWidth(False)
    symbol_layer.setInterpolatedWidth(interpolated_width)
    interpolated_color = QgsInterpolatedLineColor()
    interpolated_color.setColoringMethod(QgsInterpolatedLineColor.ColorRamp)
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
    interpolated_color.setColor(shader)
    symbol_layer.setInterpolatedColor(interpolated_color)
    symbol_layer.setDataDefinedProperty(
        QgsSymbolLayer.PropertyLineStartColorValue, QgsProperty.fromField("measure_at_start")
    )
    symbol_layer.setDataDefinedProperty(
        QgsSymbolLayer.PropertyLineEndColorValue, QgsProperty.fromField("measure_at_end")
    )
    widget.setSymbolLayer(symbol_layer)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "interpolatedlinesymbollayerwidgetvariablelinecolor.png").as_posix())

    return {
        "interpolatedlinesymbollayerwidgetvariablelinewidth.png": "QgsInterpolatedLineSymbolLayerWidget showing variable line width",
        "interpolatedlinesymbollayerwidgetvariablelinecolor.png": "QgsInterpolatedLineSymbolLayerWidget showing variable line color",
    }
