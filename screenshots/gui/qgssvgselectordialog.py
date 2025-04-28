from pathlib import Path

from qgis.gui import QgsSvgSelectorDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsSvgSelectorDialog()

    im = ScreenshotUtils.capture_dialog(widget, width=590, height=400)
    im.save((dest_path / "svgselectordialog.png").as_posix())

    return {"svgselectordialog.png": "QgsSvgSelectorDialog"}
