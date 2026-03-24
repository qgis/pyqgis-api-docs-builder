from pathlib import Path

from qgis.core import QgsMarkerSymbol, QgsRuleBasedRenderer, QgsStyle, QgsVectorLayer
from qgis.gui import QgsPanelWidgetStack, QgsRuleBasedRendererWidget
from qgis.PyQt.QtCore import QItemSelectionModel
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QTreeView

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    layer = QgsVectorLayer("Point", "Point Layer", "memory")
    symbol = QgsMarkerSymbol.createSimple({})
    symbol.setColor(QColor(120, 185, 15))
    root_rule = QgsRuleBasedRenderer.Rule(None)
    child_rule = QgsRuleBasedRenderer.Rule(
        symbol.clone(),
        filterExp='"category"=4',
        label="Protected species",
        description="Category matching protected species",
    )
    root_rule.appendChild(child_rule)
    symbol.setColor(QColor(215, 190, 65))
    child_rule = QgsRuleBasedRenderer.Rule(
        symbol.clone(),
        filterExp='"category"=5',
        label="Invasive species",
        description="Category matching invasive species",
    )
    root_rule.appendChild(child_rule)
    symbol.setColor(QColor(180, 30, 30))
    child_rule = QgsRuleBasedRenderer.Rule(
        symbol.clone(),
        filterExp='"category"=3',
        label="Endangered species",
        description="Category matching endangered species",
    )
    root_rule.appendChild(child_rule)

    layer.setRenderer(QgsRuleBasedRenderer(root_rule))
    widget = QgsRuleBasedRendererWidget(layer, QgsStyle.defaultStyle(), layer.renderer())
    # need to emulate stacked panels here -- we don't want edit rules to open a modal dialog and block the script
    stack = QgsPanelWidgetStack()
    stack.setMainPanel(widget)
    widget.setDockMode(True)

    view = widget.findChildren(QTreeView)[0]
    model = view.model()
    view.selectionModel().select(
        model.index(0, 0),
        QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows,
    )
    view.selectionModel().setCurrentIndex(
        model.index(0, 0), QItemSelectionModel.SelectionFlag.Select
    )

    im = ScreenshotUtils.capture_widget(stack, width=590, height=650)
    im.save((dest_path / "rulebasedrendererwidget.png").as_posix())

    widget.editRule()

    im = ScreenshotUtils.capture_widget(stack, width=590, height=650)
    im.save((dest_path / "rulebasedrendererwidgeteditrule.png").as_posix())

    return {
        "rulebasedrendererwidget.png": "QgsRuleBasedRendererWidget in the default state",
        "rulebasedrendererwidgeteditrule.png": "QgsRuleBasedRendererWidget when editing a rule",
    }
