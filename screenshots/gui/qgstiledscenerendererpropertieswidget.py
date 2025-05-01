from pathlib import Path

from qgis.core import QgsStyle, QgsTiledSceneLayer, QgsTiledSceneTextureRenderer
from qgis.gui import QgsTiledSceneRendererPropertiesWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsTiledSceneLayer("")
    layer.setRenderer(QgsTiledSceneTextureRenderer())
    widget = QgsTiledSceneRendererPropertiesWidget(layer, QgsStyle.defaultStyle())

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "tiledscenerendererpropertieswidget.png").as_posix())

    return {"tiledscenerendererpropertieswidget.png": "QgsTiledSceneRendererPropertiesWidget"}
