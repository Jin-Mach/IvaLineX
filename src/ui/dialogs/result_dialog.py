from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QFormLayout, QDialogButtonBox, QHBoxLayout, QWidget

from src.utilities.error_handler import ErrorHandler


# noinspection PyAttributeOutsideInit
class ResultDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("resultDialog")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 5, 20, 5)
        self.result_label_text = QLabel()
        self.result_label_text.setObjectName("resultLabelText")
        self.result_label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        self.result_label_text.setFont(font)
        self.result_layout = QFormLayout()
        self.code_result_text = QLabel()
        self.code_result_text.setObjectName("codeResultText")
        self.code_result_value = QLabel()
        self.empty_result_text = QLabel()
        self.empty_result_text.setObjectName("emptyResultText")
        self.empty_result_value = QLabel()
        self.comments_result_text = QLabel()
        self.comments_result_text.setObjectName("commentsResultText")
        self.comments_result_value = QLabel()
        time_layout = QHBoxLayout()
        self.time_label_text = QLabel()
        self.time_label_text.setObjectName("timeLabelText")
        self.time_label_result = QLabel()
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.reject)
        self.result_layout.addRow(self.code_result_text, self.code_result_value)
        time_layout.addWidget(self.time_label_text)
        time_layout.addWidget(self.time_label_result)
        time_layout.addStretch()
        main_layout.addWidget(self.result_label_text)
        main_layout.addSpacing(15)
        main_layout.addLayout(self.result_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(time_layout)
        main_layout.addWidget(button_box)
        return main_layout

    def setup_dialog(self, label_text: str, code_text: str, empty_text: str, comments_text: str, button_text: str,
                     timer_text: str, setup: dict[str, dict[str, Any]]) -> None:
        self.result_label_text.setText(label_text)
        self.code_result_text.setText(code_text)
        self.empty_result_text.setText(empty_text)
        self.comments_result_text.setText(comments_text)
        self.empty_result_text.setVisible(setup.get("python_settings").get("emptyRowsCheckboxUser", False))
        self.empty_result_value.setVisible(setup.get("python_settings").get("emptyRowsCheckboxUser", False))
        self.comments_result_text.setVisible(setup.get("python_settings").get("commentsCheckboxUser", False))
        self.comments_result_value.setVisible(setup.get("python_settings").get("commentsCheckboxUser", False))
        self.time_label_text.setText(timer_text)
        self.close_button.setText(button_text)

    def on_finished(self, results: dict[str, int], timer: str) -> None:
        try:
            self.code_result_value.setText(str(results.get("code", "Unknow")))
            if self.empty_result_text.isVisible():
                self.empty_result_value.setText(str(results.get("empty", "Unknow")))
                self.result_layout.addRow(self.empty_result_text, self.empty_result_value)
            if self.comments_result_text.isVisible():
                self.comments_result_value.setText(str(results.get("comments", "Unknow")))
                self.result_layout.addRow(self.comments_result_text, self.comments_result_value)
            self.time_label_result.setText(timer)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.objectName())

    def showEvent(self, event) -> None:
        self.setFixedSize(self.width(), self.height())
        super().showEvent(event)