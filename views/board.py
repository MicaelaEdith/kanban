from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from models import storage
from widgets.column import ColumnWidget
from translations import t


class Board(QWidget):
    back_clicked = Signal()

    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id
        self.project = storage.get_project(project_id)
        self.columns = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(16)

        top_bar = QHBoxLayout()

        btn_back = QPushButton(t("back"))
        btn_back.setStyleSheet("""
            QPushButton {
                background: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                color: #555;
            }
            QPushButton:hover {
                background: #f0f0f0;
                border-color: #999;
            }
        """)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.back_clicked.emit)
        top_bar.addWidget(btn_back)

        title = QLabel(self.project["name"])
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #333;")
        top_bar.addWidget(title)
        top_bar.addStretch()

        layout.addLayout(top_bar)

        input_bar = QFrame()
        input_bar.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 4px;
            }
        """)
        input_layout = QHBoxLayout(input_bar)
        input_layout.setContentsMargins(8, 8, 8, 8)

        self.input_task = QLineEdit()
        self.input_task.setPlaceholderText(t("task_placeholder"))
        self.input_task.returnPressed.connect(self._add_task)
        self.input_task.setStyleSheet("""
            QLineEdit {
                border: none;
                font-size: 14px;
                padding: 8px;
                color: #555;
                background: transparent;
            }
            QLineEdit::placeholder {
                color: #999;
            }
        """)
        input_layout.addWidget(self.input_task)

        btn_add = QPushButton(t("add"))
        btn_add.setFixedWidth(110)
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #388e3c;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2e7d32;
            }
        """)
        btn_add.clicked.connect(self._add_task)
        input_layout.addWidget(btn_add)

        layout.addWidget(input_bar)

        columns_frame = QFrame()
        columns_frame.setStyleSheet("QFrame { border: none; }")
        columns_layout = QHBoxLayout(columns_frame)
        columns_layout.setContentsMargins(0, 0, 0, 0)
        columns_layout.setSpacing(12)

        for col_id in ["por_hacer", "en_progreso", "hecho"]:
            tasks = self.project["columns"].get(col_id, [])
            col = ColumnWidget(col_id, tasks, on_change=self._auto_save)
            self.columns[col_id] = col
            columns_layout.addWidget(col)

        layout.addWidget(columns_frame, 1)

    def _add_task(self):
        text = self.input_task.text().strip()
        if not text:
            return
        self.columns["por_hacer"].add_card(text)
        self.input_task.clear()
        self._auto_save()

    def _auto_save(self):
        columns_data = {}
        for col_id, col in self.columns.items():
            columns_data[col_id] = col.get_tasks()
        storage.save_board(self.project_id, columns_data)
