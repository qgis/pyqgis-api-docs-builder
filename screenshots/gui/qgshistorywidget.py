from pathlib import Path

from qgis.core import Qgis
from qgis.gui import (
    QgsAbstractHistoryProvider,
    QgsHistoryEntry,
    QgsHistoryEntryNode,
    QgsHistoryProviderRegistry,
    QgsHistoryWidget,
)
from qgis.PyQt.QtCore import QDateTime, Qt

from screenshots.utils import ScreenshotUtils


class DummyProviderNode(QgsHistoryEntryNode):

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def data(self, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.text


class DummyProvider(QgsAbstractHistoryProvider):

    def id(self):
        return "dummy"

    def createNodeForEntry(self, entry, context):
        return DummyProviderNode(entry.entry["text"])


def __generate_screenshots(dest_path: Path):
    registry = QgsHistoryProviderRegistry()
    registry.addProvider(DummyProvider())
    registry.clearHistory(Qgis.HistoryProviderBackend.LocalProfile, "dummy")
    registry.addEntry(
        QgsHistoryEntry("dummy", QDateTime(2020, 5, 1, 12, 1, 15), {"text": "First event"})
    )
    registry.addEntry(
        QgsHistoryEntry("dummy", QDateTime(2020, 5, 2, 12, 1, 15), {"text": "Second event"})
    )
    registry.addEntry(
        QgsHistoryEntry("dummy", QDateTime(2020, 4, 2, 12, 1, 15), {"text": "Third event"})
    )
    widget = QgsHistoryWidget("dummy", registry=registry)

    im = ScreenshotUtils.capture_widget(widget, width=490, padding=2)
    im.save((dest_path / "historywidget.png").as_posix())

    return {"historywidget.png": "QgsHistoryWidget"}
