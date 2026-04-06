from pathlib import Path

from qgis.gui import QgsCodeEditorHTML

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCodeEditorHTML()
    widget.setText("""<html>
  <head>
    <title>QGIS</title>
  </head>
  <body>
    <h1>QGIS Rocks!</h1>
    <img src="qgis.png" style="width: 100px" />
    <!--Sample comment-->
    <p>Sample paragraph</p>
    <!--A search result-->
  </body>
</html>""")
    widget.setCursorPosition(2, 4)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditorhtml.png").as_posix())

    return {"codeeditorhtml.png": "QgsCodeEditorHTML containing sample HTML"}
