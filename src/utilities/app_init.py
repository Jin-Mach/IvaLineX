from typing import TYPE_CHECKING

from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger
from src.utilities.settings_provider import SettingsProvider

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow


def application_init(main_window: "MainWindow") -> bool:
    logger = get_logger()
    try:
        SettingsProvider.set_toml_basic(LanguageProvider.get_language_code)
        toml_data = SettingsProvider.get_toml_data()
        language = toml_data["language_settings"]["languageUser"]
        init_methods = [("apply_main_window_text", lambda: LanguageProvider.apply_ui_text(main_window, language)),
                        ("apply_main_window_config", lambda: SettingsProvider.apply_main_window_config(main_window))]
        for name, method in init_methods:
            if not method():
                logger.error(f"App init method error: {name}", exc_info=True)
                return False
        return True
    except Exception as e:
        logger.error(f"App init error: {e}", exc_info=True)
        return False