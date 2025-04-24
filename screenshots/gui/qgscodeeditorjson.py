from pathlib import Path

from qgis.gui import QgsCodeEditorJson

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCodeEditorJson()
    widget.setText(
        """{
  "user": {
    "id": 103,
    "name": "Sarah Jones",
    "contact": {
      "email": "sarah@example.com",
      "phone": "555-1234"
    }
  },
  "status": "active"
}"""
    )
    widget.setCursorPosition(2, 4)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditorjson.png").as_posix())

    return {"codeeditorjson.png": "QgsCodeEditorJson containing sample JSON"}
