from pathlib import Path

from qgis.core import QgsFeature, QgsVectorLayer
from qgis.gui import QgsAttributeDialog, QgsAttributeEditorContext, QgsGui

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    QgsGui.editorWidgetRegistry().initEditors()
    uri = "point?crs=epsg:4326&field=id:integer&field=description:string&field=category:string&field=quantity:int"
    layer = QgsVectorLayer(uri, "My Layer", "memory")
    feature = QgsFeature(layer.fields())
    feature.setAttributes([5, "Sample feature", "Transportation", 100])

    context = QgsAttributeEditorContext()
    dlg = QgsAttributeDialog(layer, feature, False, None, True, context)

    im = ScreenshotUtils.capture_dialog(dlg, width=350, height=250, show_max=True, show_min=True)
    im.save((dest_path / "attributedialog.png").as_posix())

    return {
        "attributedialog.png": "QgsAttributeDialog in QgsAttributeEditorContext.Mode.SingleEditMode"
    }
