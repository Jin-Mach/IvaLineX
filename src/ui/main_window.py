from PyQt6.QtWidgets import QMainWindow

from src.utilities.language_provider import LanguageProvider


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainWindow")
        self.setFixedSize(500, 300)
        LanguageProvider.set_ui_text(self)