import sys
import traceback

from PyQt6.QtWidgets import QApplication

from src.ui.dialogs.error_dialog import ErrorDialog
from src.ui.main_window import MainWindow
from src.utilities.app_init import application_init
from src.utilities.logger_provider import get_logger

logger = get_logger()


def create_app() -> None:
    try:
        application = QApplication(sys.argv)
        main_window = MainWindow()
        if not application_init(main_window):
            raise RuntimeError("Application initialization failed.")
        main_window.show()
        sys.exit(application.exec())
    except Exception as e:
        logger.error(f"create_app method error: {e}")
        dialog = ErrorDialog("An unexpected error occurred during application startup.",
                             traceback.format_exc(), show_details_button=False)
        if dialog.exec() == dialog.DialogCode.Rejected:
            sys.exit(1)