import traceback

from PyQt6.QtWidgets import QApplication

from src.ui.dialogs.error_dialog import ErrorDialog
from src.utilities.logger_provider import get_logger


class ErrorHandler:
    logger = get_logger()

    @staticmethod
    def exception_handler(exception: Exception, class_name: str = "Global") -> None:
        ErrorHandler.logger.error(f"{class_name}: {exception}", exc_info=True)
        from src.utilities.helpers import Helpers
        from src.core.providers.language_provider import LanguageProvider
        error_text = Helpers.get_exception_text(exception)
        if not error_text:
            error_text = exception
        parent = QApplication.activeWindow()
        dialog = ErrorDialog(error_text, traceback.format_exc(), parent)
        dialog_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, dialog.objectName())
        dialog.set_ui_text(dialog_text.get(f"{dialog.details_button.objectName()}Show", "Show details"),
                           dialog_text.get(f"{dialog.details_button.objectName()}Hide", "Hide details"),
                           dialog_text.get(dialog.close_button.objectName(), "Close"))
        dialog.exec()