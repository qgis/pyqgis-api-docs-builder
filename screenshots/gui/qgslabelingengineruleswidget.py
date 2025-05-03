from pathlib import Path

from qgis.core import (
    QgsLabelingEngineRuleAvoidLabelOverlapWithFeature,
    QgsLabelingEngineRuleMinimumDistanceLabelToLabel,
)
from qgis.gui import QgsLabelingEngineRulesWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsLabelingEngineRulesWidget()
    rule1 = QgsLabelingEngineRuleAvoidLabelOverlapWithFeature()
    rule2 = QgsLabelingEngineRuleMinimumDistanceLabelToLabel()
    widget.setRules([rule1, rule2])
    im = ScreenshotUtils.capture_widget(widget, width=390)
    im.save((dest_path / "labelengineruleswidget.png").as_posix())

    return {"labelengineruleswidget.png": "QgsLabelingEngineRulesWidget"}
