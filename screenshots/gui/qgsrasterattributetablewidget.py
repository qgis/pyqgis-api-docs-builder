from pathlib import Path

from qgis.core import Qgis, QgsRasterAttributeTable, QgsRasterLayer
from qgis.gui import QgsRasterAttributeTableWidget
from qgis.PyQt.QtCore import QVariant

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer_path = (Path(__file__).parent / ".." / "resources" / "landsat.tif").as_posix()
    layer = QgsRasterLayer(layer_path, "Raster Layer")

    rat = QgsRasterAttributeTable()
    rat.appendField(
        QgsRasterAttributeTable.Field(
            "Value", Qgis.RasterAttributeTableFieldUsage.MinMax, QVariant.Int
        )
    )
    rat.appendField(
        QgsRasterAttributeTable.Field(
            "Count", Qgis.RasterAttributeTableFieldUsage.PixelCount, QVariant.Int
        )
    )
    rat.appendField(
        QgsRasterAttributeTable.Field(
            "Class", Qgis.RasterAttributeTableFieldUsage.Name, QVariant.String
        )
    )

    rat.appendField(
        QgsRasterAttributeTable.Field("Red", Qgis.RasterAttributeTableFieldUsage.Red, QVariant.Int)
    )
    rat.appendField(
        QgsRasterAttributeTable.Field(
            "Green", Qgis.RasterAttributeTableFieldUsage.Green, QVariant.Int
        )
    )
    rat.appendField(
        QgsRasterAttributeTable.Field(
            "Blue", Qgis.RasterAttributeTableFieldUsage.Blue, QVariant.Int
        )
    )

    data_rows = [
        [0, 1, "Arid", 0, 10, 100],
        [2, 1, "Wetland", 100, 20, 0],
        [4, 2, "Urban", 200, 30, 50],
    ]

    for row in data_rows:
        rat.appendRow(row)
    rat.setDirty(False)
    layer.dataProvider().setAttributeTable(1, rat)

    widget = QgsRasterAttributeTableWidget(None, layer, 1)

    im = ScreenshotUtils.capture_widget(widget, width=590)
    im.save((dest_path / "rasterattributetablewidget.png").as_posix())

    return {"rasterattributetablewidget.png": "QgsRasterAttributeTableWidget"}
