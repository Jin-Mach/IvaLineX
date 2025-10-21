from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QProgressBar


# noinspection PyAttributeOutsideInit
class ProgressDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("progressDialog")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(True)
        self.progress_bar.setFixedHeight(15)
        main_layout.addWidget(self.text_label)
        main_layout.addWidget(self.progress_bar)
        return main_layout

    def setup_dialog(self, label_text: str, max_value: int, ) -> None:
        self.text_label.setText(label_text)
        self.progress_bar.setRange(0, max_value)
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())