import sys

from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.utilities.app_init import application_init
from src.utilities.logger_provider import get_logger


def create_app() -> None:
    logger = get_logger()
    application = QApplication(sys.argv)
    main_window = MainWindow()
    if not application_init(main_window):
        logger.error("Error in create_app method.", exc_info=True)
        sys.exit(1)
    main_window.show()
    sys.exit(application.exec())