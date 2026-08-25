from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame, QWidget
from PySide6.QtCore import Qt
from widgets.task_card import TaskCard
from translations import t


class ColumnWidget(QFrame):
    COLUMN_KEYS = {
        "por_hacer": "column_todo",
        "en_progreso": "column_progress",
        "hecho": "column_done"
    }

    COLUMN_COLORS = {
        "por_hacer": "#e3f2fd",
        "en_progreso": "#fff3e0",
        "hecho": "#e8f5e9"
    }

    HEADER_COLORS = {
        "por_hacer": "#1976d2",
        "en_progreso": "#f57c00",
        "hecho": "#388e3c"
    }

    def __init__(self, column_id, tasks, on_change):
        super().__init__()
        self.column_id = column_id
        self.on_change = on_change
        self.setMinimumWidth(280)
        self.setMaximumWidth(400)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COLUMN_COLORS[column_id]};
                border-radius: 10px;
                border: 1px solid #ccc;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        header = QLabel(t(self.COLUMN_KEYS[column_id]))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"""
            background-color: {self.HEADER_COLORS[column_id]};
            color: white;
            border-radius: 6px;
            padding: 8px;
            font-size: 14px;
            font-weight: bold;
        """)
        layout.addWidget(header)

        self.count_label = QLabel()
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_label.setStyleSheet("border: none; color: #666; font-size: 11px;")
        layout.addWidget(self.count_label)

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(4)
        self.cards_layout.addStretch()

        self.setAcceptDrops(True)

        scroll = QFrame()
        scroll.setStyleSheet("QFrame { border: none; background: transparent; }")
        scroll_layout = QVBoxLayout(scroll)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(self.cards_container)

        layout.addWidget(scroll, 1)

        for task in tasks:
            self.add_card(task)

        self._update_count()

    def _update_count(self):
        count = self.cards_layout.count() - 1
        key = "task_count_singular" if count == 1 else "task_count_plural"
        self.count_label.setText(t(key, count=count))

    def add_card(self, text):
        card = TaskCard(text, self, on_delete=self._remove_card)
        self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
        self._update_count()

    def _remove_card(self, card):
        self.cards_layout.removeWidget(card)
        card.deleteLater()
        self._update_count()
        self._emit_change()

    def get_tasks(self):
        tasks = []
        for i in range(self.cards_layout.count()):
            widget = self.cards_layout.itemAt(i).widget()
            if isinstance(widget, TaskCard):
                tasks.append(widget.text)
        return tasks

    def _emit_change(self):
        if self.on_change:
            self.on_change()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.COLUMN_COLORS[self.column_id]};
                    border-radius: 10px;
                    border: 2px dashed #666;
                }}
            """)

    def dragLeaveEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COLUMN_COLORS[self.column_id]};
                border-radius: 10px;
                border: 1px solid #ccc;
            }}
        """)

    def dropEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COLUMN_COLORS[self.column_id]};
                border-radius: 10px;
                border: 1px solid #ccc;
            }}
        """)

        text = event.mimeData().text()
        if text:
            self.add_card(text)
            self._emit_change()

            source = event.source()
            if source and isinstance(source, TaskCard):
                source.column_widget._remove_card(source)

            event.acceptProposedAction()
