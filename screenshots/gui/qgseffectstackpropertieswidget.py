from pathlib import Path

from qgis.core import QgsApplication
from qgis.gui import QgsEffectStackPropertiesWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    stack = QgsApplication.paintEffectRegistry().defaultStack()
    widget = QgsEffectStackPropertiesWidget(stack)

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "effectstackpropertieswidget.png").as_posix())

    return {"effectstackpropertieswidget.png": "QgsEffectStackPropertiesWidget"}
