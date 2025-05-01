from pathlib import Path

from qgis.core import (
    Qgis,
    QgsLayoutItemLabel,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsPrintLayout,
    QgsProject,
)
from qgis.gui import QgsCollapsibleGroupBoxBasic, QgsLayoutItemPropertiesWidget
from qgis.PyQt import sip
from qgis.PyQt.QtWidgets import QWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    project = QgsProject()
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    label_item = QgsLayoutItemLabel(layout)
    label_item.setText("My label")
    label_item.attemptResize(QgsLayoutSize(15, 10, Qgis.LayoutUnit.Centimeters))
    label_item.attemptMove(QgsLayoutPoint(5, 7.5, Qgis.LayoutUnit.Centimeters))
    layout.addLayoutItem(label_item)
    widget = QgsLayoutItemPropertiesWidget(None, label_item)
    widget.setMasterLayout(layout)

    general_opts = sip.cast(
        widget.findChild(QWidget, "mGeneralOptionsGroupBox"), QgsCollapsibleGroupBoxBasic
    )
    general_opts.setCollapsed(False)
    transforms = sip.cast(
        widget.findChild(QWidget, "mTransformsGroupBox"), QgsCollapsibleGroupBoxBasic
    )
    transforms.setCollapsed(False)

    im = ScreenshotUtils.capture_widget(widget, width=490)
    im.save((dest_path / "layoutitempropertieswidget.png").as_posix())
    del widget
    del layout

    return {"layoutitempropertieswidget.png": "QgsLayoutItemPropertiesWidget"}
