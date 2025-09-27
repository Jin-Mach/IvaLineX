from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QDialogButtonBox


# noinspection PyUnresolvedReferences
class AboutDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("aboutDialog")
        self.setFixedSize(250, 150)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.about_label_text = QLabel()
        self.about_label_text.setObjectName("aboutLabelText")
        self.about_label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        self.close_button.setObjectName("closeButton")
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.about_label_text)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self, title: str, label_text: str, button_text: str) -> None:
        self.setWindowTitle(title)
        self.about_label_text.setText(label_text)
        self.close_button.setText(button_text)