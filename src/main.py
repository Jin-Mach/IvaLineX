import sys

from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.utilities.app_init import application_init
from src.utilities.error_handler import ErrorHandler


def create_app() -> None:
    try:
        application = QApplication(sys.argv)
        main_window = MainWindow()
        if not application_init(main_window):
            raise RuntimeError("Application initialization failed.")
        main_window.show()
        sys.exit(application.exec())
    except Exception as e:
        ErrorHandler.exception_handler(e, "createApp")
        sys.exit(1)