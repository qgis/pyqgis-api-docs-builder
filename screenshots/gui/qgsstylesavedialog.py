from pathlib import Path

from qgis.gui import QgsStyleSaveDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsStyleSaveDialog()

    im = ScreenshotUtils.capture_dialog(widget, width=590)
    im.save((dest_path / "stylesavedialog.png").as_posix())

    return {"stylesavedialog.png": "QgsStyleSaveDialog"}
