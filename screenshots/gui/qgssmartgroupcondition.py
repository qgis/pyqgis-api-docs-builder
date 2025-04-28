from pathlib import Path

from qgis.gui import QgsSmartGroupCondition

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsSmartGroupCondition(1)

    im = ScreenshotUtils.capture_widget(widget, width=590, height=750)
    im.save((dest_path / "smartgroupcondition.png").as_posix())

    return {"smartgroupcondition.png": "QgsSmartGroupCondition"}
