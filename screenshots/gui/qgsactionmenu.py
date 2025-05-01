from pathlib import Path

from qgis.core import Qgis, QgsAction, QgsVectorLayer
from qgis.gui import QgsActionMenu

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    uri = "point?crs=epsg:4326&field=id:integer"
    layer = QgsVectorLayer(uri, "Scratch point layer", "memory")
    for action_text in (
        "Copy feature ID",
        "Show attachments in external viewer",
        "View on OpenStreetMap",
    ):
        layer.actions().addAction(QgsAction(Qgis.AttributeActionType.Generic, action_text, ""))
    menu = QgsActionMenu(layer, 5, None)

    im = ScreenshotUtils.capture_widget(menu)
    im.save((dest_path / "actionmenu.png").as_posix())

    return {"actionmenu.png": "QgsActionMenu showing some sample actions for a feature"}
