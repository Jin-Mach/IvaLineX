from PyQt6.QtWidgets import QMessageBox


class InfoMessageBox(QMessageBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("infoMessageBox")
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.button = self.button(QMessageBox.StandardButton.Ok)

    def set_ui_text(self, text: str, icon: QMessageBox.Icon, button_text: str) -> None:
        self.setText(text)
        self.setIcon(icon)
        self.button.setText(button_text)