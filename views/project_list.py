from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QHBoxLayout, QMessageBox,
    QMenu, QInputDialog, QComboBox
)
from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QDrag, QPixmap
from models import storage
from translations import t, set_language, get_language, LANGUAGES, LANGUAGE_NAMES


class DraggableCard(QFrame):
    def __init__(self, project, on_click, on_delete, on_rename, parent_list):
        super().__init__()
        self.project = project
        self.on_click = on_click
        self.on_delete = on_delete
        self.on_rename = on_rename
        self.parent_list = parent_list
        self._drag_start_pos = None

        self.setFixedHeight(60)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        self.setAcceptDrops(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QFrame:hover {
                border-color: #1976d2;
                background-color: #f8faff;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 8, 8)

        name_btn = QPushButton(project["name"])
        name_btn.setStyleSheet("""
            QPushButton {
                border: none;
                text-align: left;
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
            QPushButton:hover {
                color: #1976d2;
            }
        """)
        name_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        name_btn.clicked.connect(lambda: on_click(project["id"]))
        layout.addWidget(name_btn, 1)

        btn_delete = QPushButton(t("delete"))
        btn_delete.setFixedWidth(90)
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #ffebee;
                color: #e53935;
                border: 1px solid #ffcdd2;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e53935;
                color: white;
            }
        """)
        btn_delete.clicked.connect(lambda: on_delete(project["id"], project["name"]))
        layout.addWidget(btn_delete)

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
                font-size: 13px;
                color: #333;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
        """)
        rename_action = menu.addAction(t("rename"))
        action = menu.exec(self.mapToGlobal(pos))
        if action == rename_action:
            self.on_rename(self.project["id"], self.project["name"])

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
        mime.setData("application/x-project-card", self.project["id"].encode())

        pixmap = QPixmap(self.size())
        self.render(pixmap)

        drag.setMimeData(mime)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.position().toPoint())
        drag.exec(Qt.DropAction.MoveAction)
        self._drag_start_pos = None

    def mouseReleaseEvent(self, event):
        self._drag_start_pos = None
        super().mouseReleaseEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-project-card"):
            event.acceptProposedAction()
            self.setStyleSheet("""
                QFrame {
                    background: white;
                    border: 2px dashed #1976d2;
                    border-radius: 8px;
                }
            """)

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QFrame:hover {
                border-color: #1976d2;
                background-color: #f8faff;
            }
        """)

    def dropEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QFrame:hover {
                border-color: #1976d2;
                background-color: #f8faff;
            }
        """)
        if event.mimeData().hasFormat("application/x-project-card"):
            dragged_id = event.mimeData().data("application/x-project-card").data().decode()
            target_id = self.project["id"]
            if dragged_id != target_id:
                self.parent_list._reorder_projects(dragged_id, target_id)
            event.acceptProposedAction()


class ProjectList(QWidget):
    project_opened = Signal(str)
    language_changed = Signal()

    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        top_row = QHBoxLayout()

        title = QLabel(t("boards"))
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #333; padding-left: 4px;")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_row.addWidget(title)

        top_row.addStretch()

        self.lang_combo = QComboBox()
        for lang in LANGUAGES:
            self.lang_combo.addItem(LANGUAGE_NAMES[lang], lang)
        current_idx = LANGUAGES.index(get_language())
        self.lang_combo.setCurrentIndex(current_idx)
        self.lang_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 6px 28px 6px 12px;
                font-size: 13px;
                color: #555;
                background: white;
                min-width: 90px;
            }
            QComboBox:hover {
                border-color: #1976d2;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #999;
                width: 0;
                height: 0;
                margin-right: 8px;
            }
        """)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)
        top_row.addWidget(self.lang_combo)

        layout.addLayout(top_row)

        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(8, 8, 8, 8)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText(t("project_name_placeholder"))
        self.input_name.returnPressed.connect(self._create_project)
        self.input_name.setStyleSheet("""
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
        input_layout.addWidget(self.input_name)

        btn_create = QPushButton(t("create"))
        btn_create.setFixedWidth(100)
        btn_create.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        btn_create.clicked.connect(self._create_project)
        input_layout.addWidget(btn_create)

        layout.addWidget(input_frame)

        self.projects_container = QVBoxLayout()
        self.projects_container.setSpacing(8)
        layout.addLayout(self.projects_container)

        layout.addStretch()

    def _on_language_changed(self, index):
        lang = self.lang_combo.currentData()
        set_language(lang)
        storage.save_language(lang)
        self.language_changed.emit()
        self._rebuild_ui()

    def _rebuild_ui(self):
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

        top_row = QHBoxLayout()

        title = QLabel(t("boards"))
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #333; padding-left: 4px;")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_row.addWidget(title)

        top_row.addStretch()

        self.lang_combo = QComboBox()
        for lang in LANGUAGES:
            self.lang_combo.addItem(LANGUAGE_NAMES[lang], lang)
        current_idx = LANGUAGES.index(get_language())
        self.lang_combo.setCurrentIndex(current_idx)
        self.lang_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 6px 28px 6px 12px;
                font-size: 13px;
                color: #555;
                background: white;
                min-width: 90px;
            }
            QComboBox:hover {
                border-color: #1976d2;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #999;
                width: 0;
                height: 0;
                margin-right: 8px;
            }
        """)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)
        top_row.addWidget(self.lang_combo)

        layout.addLayout(top_row)

        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(8, 8, 8, 8)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText(t("project_name_placeholder"))
        self.input_name.returnPressed.connect(self._create_project)
        self.input_name.setStyleSheet("""
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
        input_layout.addWidget(self.input_name)

        btn_create = QPushButton(t("create"))
        btn_create.setFixedWidth(100)
        btn_create.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        btn_create.clicked.connect(self._create_project)
        input_layout.addWidget(btn_create)

        layout.addWidget(input_frame)

        self.projects_container = QVBoxLayout()
        self.projects_container.setSpacing(8)
        layout.addLayout(self.projects_container)

        layout.addStretch()

        self._refresh()

    def _refresh(self):
        while self.projects_container.count():
            item = self.projects_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        projects = storage.get_projects()

        if not projects:
            empty = QLabel(t("no_projects"))
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("color: #999; font-size: 14px; padding: 40px;")
            self.projects_container.addWidget(empty)
            return

        for project in projects:
            card = DraggableCard(
                project,
                on_click=lambda pid: self.project_opened.emit(pid),
                on_delete=self._delete_project,
                on_rename=self._rename_project,
                parent_list=self
            )
            self.projects_container.addWidget(card)

    def _create_project(self):
        name = self.input_name.text().strip()
        if not name:
            return
        storage.create_project(name)
        self.input_name.clear()
        self._refresh()

    def _delete_project(self, project_id, project_name):
        reply = QMessageBox.question(
            None,
            t("delete_project_title"),
            t("delete_project_msg", name=project_name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            storage.delete_project(project_id)
            self._refresh()

    def _rename_project(self, project_id, current_name):
        new_name, ok = QInputDialog.getText(
            None,
            t("rename_project_title"),
            t("rename_project_label"),
            QLineEdit.EchoMode.Normal,
            current_name
        )
        if ok and new_name.strip():
            storage.rename_project(project_id, new_name.strip())
            self._refresh()

    def _reorder_projects(self, dragged_id, target_id):
        projects = storage.get_projects()
        ids = [p["id"] for p in projects]
        if dragged_id not in ids or target_id not in ids:
            return
        ids.remove(dragged_id)
        target_idx = ids.index(target_id)
        ids.insert(target_idx, dragged_id)
        reordered = []
        project_map = {p["id"]: p for p in projects}
        for pid in ids:
            reordered.append(project_map[pid])
        storage.save_projects_order(reordered)
        self._refresh()
