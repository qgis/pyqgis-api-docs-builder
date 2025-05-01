from pathlib import Path

from qgis.core import QgsInnerGlowEffect
from qgis.gui import QgsGlowWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    effect = QgsInnerGlowEffect()
    widget = QgsGlowWidget()
    widget.setPaintEffect(effect)

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "glowwidget.png").as_posix())

    return {"glowwidget.png": "QgsGlowWidget"}
