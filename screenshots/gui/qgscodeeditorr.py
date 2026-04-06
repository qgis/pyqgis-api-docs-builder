from pathlib import Path

from qgis.gui import QgsCodeEditorR

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCodeEditorR()
    widget.setText("""# a comment
x <- 1:12
sample(x)
sample(x, replace = TRUE)
resample <- function(x, ...) x[sample.int(length(x), ...)]
resample(x[x >  8]) # length 2
a_variable <- "My string"
""")
    widget.setCursorPosition(1, 5)

    im = ScreenshotUtils.capture_widget(widget, width=530, height=320)
    im.save((dest_path / "codeeditorr.png").as_posix())

    return {"codeeditorr.png": "QgsCodeEditorR containing a sample R script"}
