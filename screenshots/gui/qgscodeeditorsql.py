from pathlib import Path

from qgis.gui import QgsCodeEditorSQL

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCodeEditorSQL()
    widget.setText("""CREATE TABLE "my_table" (
    "pk" serial NOT NULL PRIMARY KEY,
    "a_field" integer,
    "another_field" varchar(255)
);
-- Retrieve values
SELECT count(*) FROM "my_table" WHERE "a_field" > 'a value';
""")
    widget.setCursorPosition(1, 4)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditorsql.png").as_posix())

    return {"codeeditorsql.png": "QgsCodeEditorSQL containing sample SQL"}
