from pathlib import Path

from qgis.gui import QgsSvgSelectorWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsSvgSelectorWidget()

    im = ScreenshotUtils.capture_widget(widget, width=590, height=400)
    im.save((dest_path / "svgselectorwidget.png").as_posix())

    return {"svgselectorwidget.png": "QgsSvgSelectorWidget"}
