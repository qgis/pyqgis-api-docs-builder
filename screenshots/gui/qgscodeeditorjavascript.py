from pathlib import Path

from qgis.gui import QgsCodeEditorJavascript

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCodeEditorJavascript()
    widget.setText(
        """window.onAction(function update() {
    /* Do some work */
    var prevPos = closure.pos;
    element.width = 100;
    element.height = 2500;
    if (prevPos.x > 100) {
        element.x += max(100*2, 100);
    }
});"""
    )
    widget.setCursorPosition(2, 4)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditorjavascript.png").as_posix())

    return {"codeeditorjavascript.png": "QgsCodeEditorJavascript containing sample JavaScript"}
