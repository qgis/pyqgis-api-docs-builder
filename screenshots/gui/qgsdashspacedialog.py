from pathlib import Path

from qgis.gui import QgsDashSpaceDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsDashSpaceDialog([1, 2, 0.5, 0.5])

    im_collapsed = ScreenshotUtils.capture_widget(widget, width=400, padding=0)
    im_collapsed.save((dest_path / "qgsdashspacedialog.png").as_posix())

    return {"qgsdashspacedialog.png": "QgsDashSpaceDialog showing a custom dash pattern"}
