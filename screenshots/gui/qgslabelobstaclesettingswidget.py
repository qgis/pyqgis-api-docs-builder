from pathlib import Path

from qgis.gui import QgsLabelObstacleSettingsWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsLabelObstacleSettingsWidget()
    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "labelobstaclesettingswidget.png").as_posix())

    return {"labelobstaclesettingswidget.png": "QgsLabelObstacleSettingsWidget"}
