from pathlib import Path

from qgis.gui import QgsCodeEditor

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCodeEditor()
    widget.setText("Some generic code\nAdditional line")

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditor.png").as_posix())

    return {"codeeditor.png": "QgsCodeEditor"}
