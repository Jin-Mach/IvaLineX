import sys

from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def create_app() -> None:
    application = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(application.exec())