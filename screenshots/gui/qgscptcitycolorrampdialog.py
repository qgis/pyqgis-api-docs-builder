from pathlib import Path

from qgis.core import QgsCptCityArchive, QgsCptCityColorRamp
from qgis.gui import QgsCptCityColorRampDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    QgsCptCityArchive.initDefaultArchive()
    ramp = QgsCptCityColorRamp("grass/elevation", "")
    widget = QgsCptCityColorRampDialog(ramp)

    im = ScreenshotUtils.capture_dialog(widget, width=790, height=600)
    im.save((dest_path / "cptcitycolorrampdialog.png").as_posix())

    return {
        "cptcitycolorrampdialog.png": "QgsCptCityColorRampDialog showing the 'grass/elevation' color ramp"
    }
