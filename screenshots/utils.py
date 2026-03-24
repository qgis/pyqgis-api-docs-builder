"""
QGIS screenshot generation utilities
"""

from qgis.PyQt.QtCore import QRect, QSize, Qt
from qgis.PyQt.QtGui import QImage, QPainter
from qgis.PyQt.QtTest import QTest
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QStyle,
    QStyleOptionFrame,
    QStyleOptionTitleBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class ScreenshotUtils:
    """
    Utility class for screenshot generation
    """

    @staticmethod
    def capture_widget(
        widget: QWidget, width: int = 300, height: int | None = None, padding: int | None = None
    ) -> QImage:
        """
        Captures a QWidget to an image, at the specified width and height.
        """
        # create a layout for the widget
        w = QWidget()
        vl = QVBoxLayout()
        if padding is not None:
            vl.setContentsMargins(padding, padding, padding, padding)
        w.setLayout(vl)
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

        im = QImage(QSize(w.width(), min_height), QImage.Format.Format_ARGB32)
        im.fill(Qt.GlobalColor.transparent)

        painter = QPainter(im)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        w.render(painter)
        painter.end()

        w.layout().removeWidget(widget)
        widget.setParent(None)

        return im

    @staticmethod
    def capture_dialog(
        dialog: QDialog,
        width: int = 300,
        height: int | None = None,
        show_max: bool = False,
        show_min: bool = False,
    ) -> QImage:
        """
        Captures a QDialog to an image, at the specified width and height.

        Ensures that the window frame and title bar are also drawn.

        Optionally, the minimize and maximize buttons can be shown.
        """
        dialog.setFixedWidth(width)
        if height:
            dialog.setFixedHeight(height)

        style = dialog.style()
        title_bar_option = QStyleOptionTitleBar()
        title_bar_option.initFrom(dialog)
        frame_width = style.pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth, None, dialog)
        title_bar_height = style.pixelMetric(
            QStyle.PixelMetric.PM_TitleBarHeight, title_bar_option, dialog
        )
        content_rect = dialog.rect()
        dialog_rect = content_rect.adjusted(-frame_width, -frame_width, frame_width, frame_width)
        frame_rect = content_rect.adjusted(
            -frame_width, -title_bar_height, frame_width, frame_width
        )
        title_bar_rect = QRect(
            frame_rect.left(), frame_rect.top(), frame_rect.width(), title_bar_height
        )

        im = QImage(QSize(frame_rect.width(), frame_rect.height()), QImage.Format.Format_ARGB32)
        im.fill(Qt.GlobalColor.transparent)

        painter = QPainter(im)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(frame_width, title_bar_height)

        # ensure widget is ready for screenshot
        dialog.show()
        dialog.ensurePolished()
        QTest.qWait(50)

        frame_option = QStyleOptionFrame()
        frame_option.initFrom(dialog)
        frame_option.rect = dialog_rect
        frame_option.frameShape = QFrame.Shape.StyledPanel
        frame_option.state |= QStyle.StateFlag.State_Raised

        # draw frame
        style.drawPrimitive(QStyle.PrimitiveElement.PE_Frame, frame_option, painter, dialog)

        title_bar_option.rect = title_bar_rect
        title_bar_option.text = dialog.windowTitle()
        title_bar_option.state = QStyle.StateFlag.State_Active
        title_bar_option.subControls = (
            QStyle.SubControl.SC_TitleBarCloseButton | QStyle.SubControl.SC_TitleBarLabel
        )
        title_bar_option.titleBarFlags = (
            Qt.WindowType.Window
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowSystemMenuHint
            | Qt.WindowType.WindowMinMaxButtonsHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        title_bar_option.titleBarState = QStyle.StateFlag.State_Active

        # draw title bar background
        style.drawComplexControl(
            QStyle.ComplexControl.CC_TitleBar, title_bar_option, painter, dialog
        )

        # draw window title
        style.drawItemText(
            painter,
            title_bar_option.rect,
            Qt.AlignmentFlag.AlignCenter,
            dialog.palette(),
            True,
            title_bar_option.text,
        )

        # Draw window buttons (minimize, maximize, close)
        button_option = QStyleOptionTitleBar(title_bar_option)
        button_option.subControls = (
            QStyle.SubControl.SC_TitleBarCloseButton | QStyle.SubControl.SC_TitleBarLabel
        )
        if show_max:
            button_option.subControls |= QStyle.SubControl.SC_TitleBarMaxButton
        if show_min:
            button_option.subControls |= QStyle.SubControl.SC_TitleBarMinButton
        style.drawComplexControl(QStyle.ComplexControl.CC_TitleBar, button_option, painter, dialog)

        # draw actual dialog contents
        dialog.render(painter)
        painter.end()

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

        im = QImage(QSize(w.width(), min_height), QImage.Format.Format_ARGB32)
        im.fill(Qt.GlobalColor.transparent)

        painter = QPainter(im)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w.render(painter)
        popup.render(painter, targetOffset=popup_top_left)
        painter.end()

        w.layout().removeWidget(combo)
        combo.setParent(None)

        return im

    @staticmethod
    def capture_toolbutton_with_dropdown(button: QToolButton, width: int = 300) -> QImage:
        """
        Captures a QToolButton showing the menu expanded
        """
        # create a layout for the combobox
        w = QWidget()
        w.setLayout(QVBoxLayout())
        w.layout().addWidget(button)
        w.layout().addStretch()
        w.setFixedWidth(width)
        # something big enough to show all reasonable drop down heights!
        w.setFixedHeight(600)

        # ensure widget is ready for screenshot
        w.show()
        w.ensurePolished()
        QTest.qWait(50)

        menu = button.menu()
        menu.aboutToShow.emit()
        menu.show()
        menu.ensurePolished()

        popup_top_left = w.mapFromGlobal(
            button.parent().mapToGlobal(button.geometry().bottomLeft())
        )

        menu_size = menu.size()
        min_height = (
            popup_top_left.y() + menu_size.height() + w.layout().contentsMargins().bottom()
        )

        im = QImage(QSize(w.width(), min_height), QImage.Format.Format_ARGB32)
        im.fill(Qt.GlobalColor.transparent)

        painter = QPainter(im)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w.render(painter)

        menu.render(painter, targetOffset=popup_top_left)
        painter.end()

        w.layout().removeWidget(button)
        button.setParent(None)

        return im
