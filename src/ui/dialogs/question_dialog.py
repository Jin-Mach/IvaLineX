from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QDialogButtonBox


# noinspection PyTypeChecker
class QuestionDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("questionDialog")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.question_text_label = QLabel()
        self.question_text_label.setObjectName("questionTextLabel")
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.question_accept_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.question_accept_button.setObjectName("questionAcceptButton")
        self.question_cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        self.question_cancel_button.setObjectName("questionCancelButton")
        self.question_accept_button.clicked.connect(self.accept)
        self.question_cancel_button.clicked.connect(self.reject)
        main_layout.addWidget(self.question_text_label)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self, question_text: str, accept_text: str, cancel_text: str) -> None:
        self.question_text_label.setText(question_text)
        self.question_accept_button.setText(accept_text)
        self.question_cancel_button.setText(cancel_text)

    def showEvent(self, event) -> QEvent:
        self.question_cancel_button.setFocus()
        super().showEvent(event)