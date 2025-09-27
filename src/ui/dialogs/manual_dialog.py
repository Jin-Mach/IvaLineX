from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QTextEdit, QDialogButtonBox


# noinspection PyUnresolvedReferences
class ManualDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualDialog")
        self.setFixedSize(500, 500)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_edit = QTextEdit()
        self.manual_edit.setObjectName("manualEdit")
        self.manual_edit.setReadOnly(True)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        self.close_button.setObjectName("closeButton")
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.manual_edit)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self, manual_text: tuple[dict[str, str], str]) -> None:
        json_text = manual_text[0]
        self.setWindowTitle(json_text.get(f"{self.objectName()}Title", "Manual"))
        self.close_button.setText(json_text.get(self.close_button.objectName(), "Close"))
        self.manual_edit.setHtml(manual_text[1])