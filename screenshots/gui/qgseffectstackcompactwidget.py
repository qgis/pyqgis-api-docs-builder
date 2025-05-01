from pathlib import Path

from qgis.core import QgsApplication
from qgis.gui import QgsEffectStackCompactWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    stack = QgsApplication.paintEffectRegistry().defaultStack()
    widget = QgsEffectStackCompactWidget(effect=stack)

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "effectstackcompactwidget.png").as_posix())

    return {"effectstackcompactwidget.png": "QgsEffectStackCompactWidget"}
