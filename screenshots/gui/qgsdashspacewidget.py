from pathlib import Path

from qgis.gui import QgsDashSpaceWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsDashSpaceWidget([1, 2, 0.5, 0.5])

    im_collapsed = ScreenshotUtils.capture_widget(widget, width=400)
    im_collapsed.save((dest_path / "qgsdashspacewidget.png").as_posix())

    return {"qgsdashspacewidget.png": "QgsDashSpaceWidget showing a custom dash pattern"}
