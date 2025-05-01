from pathlib import Path

from qgis.core import QgsTransformEffect
from qgis.gui import QgsTransformWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    effect = QgsTransformEffect()
    widget = QgsTransformWidget()
    widget.setPaintEffect(effect)

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "transformwidget.png").as_posix())

    return {"transformwidget.png": "QgsTransformWidget"}
