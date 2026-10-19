import sys
import os

if getattr(sys, 'frozen', False):
    _base_dir = os.path.dirname(sys.executable)
    _bundled_dir = sys._MEIPASS
else:
    _base_dir = os.path.dirname(os.path.abspath(__file__))
    _bundled_dir = _base_dir

sys.path.insert(0, _base_dir)


def resource_path(relative_path):
    return os.path.join(_bundled_dir, relative_path)


from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from views.project_list import ProjectList
from views.board import Board
from models import storage
from translations import t, set_language, get_language


class KanbanApp(QMainWindow):
    def __init__(self):
        super().__init__()
        saved_lang = storage.get_language()
        set_language(saved_lang)

        self.setWindowTitle("KanbanEvent")
        self.setMinimumSize(1000, 650)
        self.resize(1200, 750)

        icon = QIcon(resource_path("icono.png"))
        self.setWindowIcon(icon)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.project_list = ProjectList()
        self.project_list.project_opened.connect(self._open_board)
        self.project_list.language_changed.connect(self._on_language_changed)
        self.stack.addWidget(self.project_list)

    def _on_language_changed(self):
        self.setWindowTitle("KanbanEvent")

    def _open_board(self, project_id):
        self.board = Board(project_id)
        self.board.back_clicked.connect(self._go_back)
        self.stack.addWidget(self.board)
        self.stack.setCurrentWidget(self.board)

    def _go_back(self):
        self.stack.removeWidget(self.board)
        self.board.deleteLater()
        self.project_list._refresh()
        self.stack.setCurrentWidget(self.project_list)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    icon = QIcon(resource_path("icono.png"))
    app.setWindowIcon(icon)

    font = app.font()
    font.setFamily("Segoe UI")
    app.setFont(font)

    window = KanbanApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
