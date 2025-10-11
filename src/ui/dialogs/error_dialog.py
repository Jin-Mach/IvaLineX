from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox


# noinspection PyTypeChecker
class ErrorDialog(QDialog):
    def __init__(self, error_text: str, traceback: str, show_details_button: bool = True, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("errorDialog")
        self.error_text = error_text
        self.traceback = traceback
        self.show_details_button = show_details_button
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        error_text_label = QLabel()
        error_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        error_text_label.setFont(font)
        error_text_label.setText(self.error_text)
        self.error_details_edit = QTextEdit()
        self.error_details_edit.setReadOnly(True)
        self.error_details_edit.setText(self.traceback)
        self.error_details_edit.setVisible(False)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.RestoreDefaults | QDialogButtonBox.StandardButton.Close)
        self.details_button = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        self.details_button.setObjectName("detailsButton")
        self.details_button.setVisible(self.show_details_button)
        self.details_button.clicked.connect(self.show_edit)
        self.close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        self.close_button.setObjectName("closeButton")
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(error_text_label)
        main_layout.addWidget(self.error_details_edit)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self, show_detail: str, hide_detail: str, close: str) -> None:
        self.show_text = show_detail
        self.hide_text = hide_detail
        self.details_button.setText(self.show_text)
        self.close_button.setText(close)

    def show_edit(self) -> None:
        if self.error_details_edit.isVisible():
            self.error_details_edit.setVisible(False)
            self.details_button.setText(self.show_text)
        else:
            self.error_details_edit.setVisible(True)
            self.details_button.setText(self.hide_text)
        self.adjustSize()