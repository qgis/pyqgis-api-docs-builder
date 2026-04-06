from pathlib import Path

from qgis.gui import QgsCodeEditorExpression

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCodeEditorExpression()
    widget.setText("""aggregate(layer:='rail_stations',
    aggregate:='collect', -- a comment
    expression:=centroid(@geometry), /* a comment */
    filter:="region_name" = attribute(@parent,'name') + 55
)""")
    widget.setCursorPosition(2, 4)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditorexpression.png").as_posix())

    return {
        "codeeditorexpression.png": "QgsCodeEditorExpression containing a sample QGIS expression"
    }
