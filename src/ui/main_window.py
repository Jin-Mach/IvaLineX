from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListView, \
    QApplication, QCheckBox

from src.controllers.dialogs_controler import DialogsController
from src.ui.widgets.menu_bar import MenuBar


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainWindow")
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.create_gui())
        self.init_window_geometry()
        self.create_connection()

    def create_gui(self) -> QWidget:
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        project_layout = QHBoxLayout()
        project_name_text_label = QLabel()
        project_name_text_label.setObjectName("projectNameTextLabel")
        self.project_name_label = QLabel("název projektu..")
        self.project_name_label.setObjectName("projectNameLabel")
        folder_layout = QHBoxLayout()
        folder_text_label = QLabel()
        folder_text_label.setObjectName("folderTextLabel")
        self.folder_line_input = QLineEdit()
        self.folder_line_input.setObjectName("folderLineInput")
        self.folder_line_input.setReadOnly(True)
        self.folder_button = QPushButton()
        self.folder_button.setObjectName("folderButton")
        folder_list_view = QListView()
        folder_list_view.setObjectName("foldersListView")
        files_layout = QHBoxLayout()
        self.save_history_checkbox = QCheckBox()
        self.save_history_checkbox.setObjectName("saveHistoryCheckBox")
        files_count_text_label = QLabel()
        files_count_text_label.setObjectName("filesCountTextLabel")
        self.files_count_label = QLabel("20")
        self.files_count_label.setObjectName("filesCountLabel")
        buttons_layout = QHBoxLayout()
        count_button = QPushButton()
        count_button.setObjectName("countButton")
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
        buttons_layout.addWidget(count_button)
        buttons_layout.addStretch()
        main_layout.addLayout(project_layout)
        main_layout.addLayout(folder_layout)
        main_layout.addWidget(folder_list_view)
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
        self.dialog_controller = DialogsController(self, self.menu_bar)
        self.folder_button.clicked.connect(self.dialog_controller.set_folder_path)