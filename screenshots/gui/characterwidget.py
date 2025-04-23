from pathlib import Path

from qgis.gui import CharacterWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = CharacterWidget()

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "characterwidget.png").as_posix())

    return {"characterwidget.png": "CharacterWidget in a default state"}
