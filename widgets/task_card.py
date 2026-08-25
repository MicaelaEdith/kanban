from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QMimeData, QPoint, QPropertyAnimation
from PySide6.QtGui import QDrag, QPixmap, QPainter


class TaskCard(QFrame):
    def __init__(self, text, column_widget, on_delete=None):
        super().__init__()
        self.text = text
        self.column_widget = column_widget
        self.on_delete = on_delete
        self._drag_start_pos = None

        self.setFixedHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                padding: 4px;
            }
            QFrame:hover {
                border-color: #90caf9;
                background-color: #f5faff;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 4, 4)

        self.label = QLabel(text)
        self.label.setStyleSheet("border: none; font-size: 13px; color: #333;")
        self.label.setWordWrap(True)
        layout.addWidget(self.label, 1)

        btn_delete = QPushButton("\u2715")
        btn_delete.setFixedSize(24, 24)
        btn_delete.setStyleSheet("""
            QPushButton {
                border: none;
                color: #999;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #e53935;
                background-color: #ffebee;
                border-radius: 12px;
            }
        """)
        btn_delete.clicked.connect(self._delete)
        layout.addWidget(btn_delete, 0, Qt.AlignmentFlag.AlignTop)

    def _delete(self):
        if self.on_delete:
            self.on_delete(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_start_pos is None:
            return

        distance = (event.position().toPoint() - self._drag_start_pos).manhattanLength()
        if distance < 10:
            return

        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(self.text)
        mime.setData("application/x-task-card", b"1")

        pixmap = QPixmap(self.size())
        self.render(pixmap)
        painter = QPainter(pixmap)
        painter.setOpacity(0.7)
        painter.end()

        drag.setMimeData(mime)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.position().toPoint())
        drag.exec(Qt.DropAction.MoveAction)

        self._drag_start_pos = None

    def mouseReleaseEvent(self, event):
        self._drag_start_pos = None
        super().mouseReleaseEvent(event)
