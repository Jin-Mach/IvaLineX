import sys
import traceback

from typing import TYPE_CHECKING

from src.core.managers.files_manager import FilesManager
from src.core.managers.language_manager import LanguageManager
from src.core.providers.language_provider import LanguageProvider
from src.ui.dialogs.error_dialog import ErrorDialog
from src.utilities.logger_provider import get_logger
from src.core.managers.settings_manager import SettingsManager
from src.core.providers.settings_provider import SettingsProvider

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow


def application_init(main_window: "MainWindow") -> bool:
    logger = get_logger()
    try:
        if not FilesManager.download_missing_files():
            dialog = ErrorDialog("Failed to download required files.\n"
                                 "Please check your internet connection and try again.",
                                 traceback.format_exc(), show_details_button=False)
            if dialog.exec() == dialog.DialogCode.Rejected:
                logger.error("app_init error: Download files failed.", exc_info=True)
                sys.exit(1)
        SettingsProvider.set_toml_basic(LanguageProvider.get_language_code)
        toml_data = SettingsProvider.get_toml_data()
        language = toml_data["language_settings"]["languageUser"]
        init_methods = [("apply_main_window_text", lambda: LanguageManager.apply_ui_text(main_window, language)),
                        ("apply_main_window_config", lambda: SettingsManager.apply_main_window_config(
                            main_window.save_history_checkbox))]
        for name, method in init_methods:
            if not method():
                logger.error(f"App init method error: {name}", exc_info=True)
                return False
        return True
    except Exception as e:
        logger.error(f"App init error: {e}", exc_info=True)
        return False