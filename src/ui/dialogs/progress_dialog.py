from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QProgressBar


# noinspection PyAttributeOutsideInit
class ProgressDialog(QDialog):
    def __init__(self, progress_text: bool, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("progressDialog")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress_text = progress_text
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(True)
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setTextVisible(self.progress_text)
        main_layout.addWidget(self.text_label)
        main_layout.addWidget(self.progress_bar)
        return main_layout

    def setup_dialog(self, label_text: str, max_value: int, finish_text: str) -> None:
        self.text_label.setText(label_text)
        self.progress_bar.setRange(0, max_value)
        if self.progress_text:
            self.progress_bar.setFormat("%p%")
            self.finish_text = finish_text
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def on_finished(self) -> None:
        self.text_label.setText(self.finish_text)
        QTimer.singleShot(500, self.close)