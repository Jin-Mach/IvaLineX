from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QApplication, QCheckBox, QAbstractItemView)

from src.controllers.controlers_service import ControllersService
from src.ui.widgets.folder_list_view import FolderListView
from src.ui.widgets.menu_bar import MenuBar


# noinspection PyUnresolvedReferences,PyAttributeOutsideInit
class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainWindow")
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.create_gui())
        self.init_window_geometry()
        self.controller_service = ControllersService(self, self.menu_bar)
        self.create_connection()

    def create_gui(self) -> QWidget:
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        project_layout = QHBoxLayout()
        project_name_text_label = QLabel()
        project_name_text_label.setObjectName("projectNameTextLabel")
        self.project_name_label = QLabel()
        self.project_name_label.setObjectName("projectNameLabel")
        font = QFont()
        font.setBold(True)
        self.project_name_label.setFont(font)
        folder_layout = QHBoxLayout()
        folder_text_label = QLabel()
        folder_text_label.setObjectName("folderTextLabel")
        self.folder_line_input = QLineEdit()
        self.folder_line_input.setObjectName("folderLineInput")
        self.folder_line_input.setReadOnly(True)
        self.folder_button = QPushButton()
        self.folder_button.setObjectName("folderButton")
        self.folder_list_view = FolderListView(self)
        self.folder_list_view.setObjectName("foldersListView")
        self.folder_list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        files_layout = QHBoxLayout()
        self.save_history_checkbox = QCheckBox()
        self.save_history_checkbox.setObjectName("saveHistoryCheckBox")
        files_count_text_label = QLabel()
        files_count_text_label.setObjectName("filesCountTextLabel")
        self.files_count_label = QLabel("20")
        self.files_count_label.setObjectName("filesCountLabel")
        buttons_layout = QHBoxLayout()
        self.count_button = QPushButton()
        self.count_button.setObjectName("countButton")
        project_layout.addWidget(project_name_text_label)
        project_layout.addWidget(self.project_name_label)
        project_layout.addStretch()
        folder_layout.addWidget(folder_text_label)
        folder_layout.addWidget(self.folder_line_input)
        folder_layout.addWidget(self.folder_button)
        files_layout.addWidget(self.save_history_checkbox)
        files_layout.addStretch()
        files_layout.addWidget(files_count_text_label)
        files_layout.addWidget(self.files_count_label)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.count_button)
        buttons_layout.addStretch()
        main_layout.addLayout(project_layout)
        main_layout.addLayout(folder_layout)
        main_layout.addWidget(self.folder_list_view)
        main_layout.addLayout(files_layout)
        main_layout.addLayout(buttons_layout)
        central_widget.setLayout(main_layout)
        return central_widget

    def init_window_geometry(self) -> None:
        self.setFixedSize(400, 500)
        screen = QApplication.primaryScreen()
        if screen:
            screen_geom = screen.availableGeometry()
            x_pos = screen_geom.width() // 2 - self.width() // 2
            y_pos = screen_geom.height() // 2 - self.height() // 2
            self.move(x_pos, y_pos)

    def create_connection(self) -> None:
        self.folder_button.clicked.connect(self.controller_service.dialog_controller.set_folder_path)