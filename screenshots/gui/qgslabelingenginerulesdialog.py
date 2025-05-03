from pathlib import Path

from qgis.core import (
    QgsLabelingEngineRuleAvoidLabelOverlapWithFeature,
    QgsLabelingEngineRuleMinimumDistanceLabelToLabel,
)
from qgis.gui import QgsLabelingEngineRulesDialog

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    dlg = QgsLabelingEngineRulesDialog()
    rule1 = QgsLabelingEngineRuleAvoidLabelOverlapWithFeature()
    rule2 = QgsLabelingEngineRuleMinimumDistanceLabelToLabel()
    dlg.setRules([rule1, rule2])
    im = ScreenshotUtils.capture_dialog(dlg, width=390, height=300)
    im.save((dest_path / "labelenginerulesdialog.png").as_posix())

    return {"labelenginerulesdialog.png": "QgsLabelingEngineRulesDialog"}
