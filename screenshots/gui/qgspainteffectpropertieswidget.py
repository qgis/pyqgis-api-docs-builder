from pathlib import Path

from qgis.core import QgsDropShadowEffect
from qgis.gui import QgsPaintEffectPropertiesWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    effect = QgsDropShadowEffect()
    widget = QgsPaintEffectPropertiesWidget(effect=effect)

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "painteffectpropertieswidget.png").as_posix())

    return {"painteffectpropertieswidget.png": "QgsPaintEffectPropertiesWidget"}
