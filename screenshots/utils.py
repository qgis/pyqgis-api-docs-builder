"""
QGIS screenshot generation utilities
"""

from qgis.PyQt.QtCore import QSize, Qt
from qgis.PyQt.QtGui import QImage, QPainter
from qgis.PyQt.QtTest import QTest
from qgis.PyQt.QtWidgets import QComboBox, QVBoxLayout, QWidget


class ScreenshotUtils:
    """
    Utility class for screenshot generation
    """

    @staticmethod
    def capture_widget(widget: QWidget, width: int = 300, height: int | None = None) -> QImage:
        """
        Captures a QWidget to an image, at the specified width and height.
        """
        # create a layout for the widget
        w = QWidget()
        w.setLayout(QVBoxLayout())
        w.layout().addWidget(widget)
        w.layout().addStretch()
        w.setFixedWidth(width)
        if height:
            w.setFixedHeight(height)

        # ensure widget is ready for screenshot
        w.show()
        w.ensurePolished()
        QTest.qWait(50)

        min_height = (
            widget.height()
            + w.layout().contentsMargins().top()
            + w.layout().contentsMargins().bottom()
        )

        im = QImage(QSize(w.width(), min_height), QImage.Format_ARGB32)
        im.fill(Qt.transparent)

        painter = QPainter(im)
        w.render(painter)
        painter.end()

        w.layout().removeWidget(widget)
        widget.setParent(None)

        return im

    @staticmethod
    def capture_combo_with_dropdown(combo: QComboBox, width: int = 300) -> QImage:
        """
        Captures a QComboBox showing the combo box control expanded
        """
        # create a layout for the combobox
        w = QWidget()
        w.setLayout(QVBoxLayout())
        w.layout().addWidget(combo)
        w.layout().addStretch()
        w.setFixedWidth(width)
        # something big enough to show all reasonable drop down heights!
        w.setFixedHeight(600)

        # ensure combo is ready for screenshot
        w.show()
        w.ensurePolished()
        combo.showPopup()
        QTest.qWait(50)

        popup = combo.findChild(QWidget)
        popup_top_left = w.mapFromGlobal(combo.parent().mapToGlobal(combo.geometry().bottomLeft()))

        combo_size = combo.size()
        popup_size = popup.size()
        min_height = (
            combo_size.height()
            + popup_size.height()
            + w.layout().contentsMargins().top()
            + w.layout().contentsMargins().bottom()
        )

        im = QImage(QSize(w.width(), min_height), QImage.Format_ARGB32)
        im.fill(Qt.transparent)

        painter = QPainter(im)
        w.render(painter)
        popup.render(painter, targetOffset=popup_top_left)
        painter.end()

        w.layout().removeWidget(combo)
        combo.setParent(None)

        return im
