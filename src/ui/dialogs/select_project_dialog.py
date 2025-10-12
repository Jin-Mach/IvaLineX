from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox


# noinspection PyTypeChecker
class SelectProjectDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("selectProjectDialog")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.select_project_label_text = QLabel()
        self.select_project_label_text.setObjectName("selectProjectLabelText")
        self.select_project_label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.projects_combobox = QComboBox()
        self.projects_combobox.setObjectName("projectsCombobox")
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Close)
        self.load_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.load_button.setObjectName("loadButton")
        self.close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        self.close_button.setObjectName("closeButton")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.select_project_label_text)
        main_layout.addWidget(self.projects_combobox)
        main_layout.addWidget(button_box)
        return  main_layout

    def set_ui_text(self, title: str, label: str, load: str, close: str) -> None:
        self.setWindowTitle(title)
        self.select_project_label_text.setText(label)
        self.load_button.setText(load)
        self.close_button.setText(close)

    def showEvent(self, event) -> None:
        self.setFixedSize(self.width(), self.height())
        return super().showEvent(event)