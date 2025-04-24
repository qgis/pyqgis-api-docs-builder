from pathlib import Path

from qgis.gui import QgsCodeEditorCSS

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCodeEditorCSS()
    widget.setText(
        """@font-face {
 font-family: DroidSans; /* A comment */
 src: url('DroidSans.ttf');
}
p.style_name:lang(en) {
 color: #F0F0F0;
 background: #600;
}
/* A search result */
ul > li, a:hover {
 line-height: 11px;
 text-decoration: underline;
}
@media print {
  a[href^=http]::after {
    content: attr(href)
  }
}"""
    )
    widget.setCursorPosition(2, 10)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditorcss.png").as_posix())

    return {"codeeditorcss.png": "QgsCodeEditorCSS containing sample CSS code"}
