from pathlib import Path

from qgis.gui import QgsColorEffectWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsColorEffectWidget()

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "coloreffectwidget.png").as_posix())

    return {"coloreffectwidget.png": "QgsColorEffectWidget"}
