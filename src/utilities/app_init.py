from PyQt6.QtWidgets import QMainWindow

from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


def application_init(main_window: QMainWindow) -> bool:
    logger = get_logger()
    try:
        language = LanguageProvider.get_language_code()
        init_methods = [("apply_ui_text", lambda: LanguageProvider.apply_ui_text([main_window], language))]
        for name, method in init_methods:
            if not method():
                logger.error(f"App init method error: {name}", exc_info=True)
                return False
        return True
    except Exception as e:
        logger.error(f"App init error: {e}", exc_info=True)
        return False