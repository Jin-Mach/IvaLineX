from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel


# noinspection PyTypeChecker
class NewProjectDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("newProjectDialog")
        self.setLayout(self.create_gui())
        self.create_connection()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.new_project_label_text = QLabel()
        self.new_project_label_text.setObjectName("newProjectLabelText")
        self.new_project_label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.project_name_edit = QLineEdit()
        self.project_name_edit.setObjectName("projectNameEdit")
        regex = QRegularExpression(r"^[A-Za-z\s]+$")
        validator = QRegularExpressionValidator(regex)
        self.project_name_edit.setValidator(validator)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Close)
        self.save_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.save_button.setObjectName("saveButton")
        self.save_button.setDisabled(True)
        self.close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        self.close_button.setObjectName("closeButton")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.new_project_label_text)
        main_layout.addWidget(self.project_name_edit)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self, title: str, label: str, save: str, close: str) -> None:
        self.setWindowTitle(title)
        self.new_project_label_text.setText(label)
        self.save_button.setText(save)
        self.close_button.setText(close)

    def showEvent(self, event) -> None:
        self.setFixedSize(self.width(), self.height())
        super().showEvent(event)

    def create_connection(self) -> None:
        self.project_name_edit.textChanged.connect(self.check_save_button)

    def check_save_button(self) -> None:
        if not self.project_name_edit.text():
            self.save_button.setDisabled(True)
        else:
            self.save_button.setDisabled(False)