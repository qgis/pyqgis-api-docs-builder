from pathlib import Path

from qgis.core import QgsLayoutItemLabel, QgsPrintLayout, QgsProject
from qgis.gui import QgsCollapsibleGroupBoxBasic, QgsLayoutItemPropertiesWidget
from qgis.PyQt import sip
from qgis.PyQt.QtWidgets import QWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    project = QgsProject()
    layout = QgsPrintLayout(project)
    label_item = QgsLayoutItemLabel(layout)
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

    return {"layoutitempropertieswidget.png": "QgsLayoutItemPropertiesWidget"}
