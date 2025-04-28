from pathlib import Path

from qgis.gui import QgsSymbolAnimationSettingsWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsSymbolAnimationSettingsWidget()

    im = ScreenshotUtils.capture_widget(widget, width=590, padding=0)
    im.save((dest_path / "symbolanimationsettingswidget.png").as_posix())

    return {"symbolanimationsettingswidget.png": "QgsSymbolAnimationSettingsWidget"}
