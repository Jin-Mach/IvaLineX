from typing import TYPE_CHECKING, Any, Callable

import pathlib
import tomllib
import tomli_w

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QWidget, QLineEdit

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow
    from src.ui.dialogs.settings_dialog import SettingsDialog

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.joinpath("config", "app_settings.toml")


# noinspection PyUnresolvedReferences
class SettingsProvider:
    class_name = "settingsProvider"

    @staticmethod
    def apply_main_window_config(main_window: "MainWindow") -> bool:
        try:
            toml_data = SettingsProvider.get_toml_data()
            if not toml_data:
                raise ValueError(f"Load toml data error.")
            history_value = toml_data.get("history_section", {}).get("historyCheckboxUser", True)
            if history_value:
                main_window.save_history_checkbox.setChecked(history_value)
            return True
        except Exception as e:
            ErrorHandler.exception_handler(e, SettingsProvider.class_name)
            return False

    @staticmethod
    def apply_settings_dialog_config(dialog: "SettingsDialog") -> None:
        try:
            toml_data = SettingsProvider.get_toml_data()
            if not toml_data:
                raise ValueError(f"Load toml data error.")
            for widget in dialog.findChildren(QWidget):
                for section in ["language_settings", "path_settings", "history_settings", "python_settings"]:
                    value = toml_data.get(section, {}).get(f"{widget.objectName()}User", {})
                    if value:
                        if hasattr(widget, "addItems"):
                            widget.clear()
                            if isinstance(value, list):
                                widget.addItems(value)
                        if hasattr(widget, "setText"):
                            if isinstance(widget, QLineEdit):
                                metrics = QFontMetrics(widget.font())
                                short_path = metrics.elidedText(value, Qt.TextElideMode.ElideLeft, widget.width())
                                widget.setText(short_path)
                                widget.setToolTip(str(value))
                            else:
                                widget.setText(str(value))
                        if hasattr(widget, "setChecked"):
                            widget.setChecked(bool(value))
        except Exception as e:
            ErrorHandler.exception_handler(e, SettingsProvider.class_name)

    @staticmethod
    def get_toml_data() -> dict[str, Any]:
        try:
            if not BASE_DIR.exists() or BASE_DIR.stat().st_size == 0:
                raise FileNotFoundError(f"Toml file not found: {BASE_DIR}")
            with open(BASE_DIR, "rb") as toml_file:
                toml_data = tomllib.load(toml_file)
                return toml_data
        except Exception as e:
            ErrorHandler.exception_handler(e, SettingsProvider.class_name)
            return {}

    @staticmethod
    def set_toml_basic(get_language: Callable[[], str]) -> None:
        try:
            toml_data = SettingsProvider.get_toml_data()
            if not toml_data:
                raise ValueError(f"Load toml data error.")
            language_section = toml_data.setdefault("language_settings", {})
            if "languageDefault" not in language_section or language_section["languageDefault"] == "":
                language = get_language()
                language_section["languageDefault"] = language
                language_section["languageUser"] = language
            LanguageProvider.usage_language = toml_data.get("language_settings", {}).get("languageUser", "en_GB")
            path_section = toml_data.setdefault("path_settings", {})
            if "folderEditDefault" not in path_section or path_section["folderEditDefault"] == "":
                path_section["folderEditDefault"] = str(BASE_DIR.parents[2])
                path_section["folderEditUser"] = str(BASE_DIR.parents[2])
            with open(BASE_DIR, "wb") as toml_file:
                tomli_w.dump(toml_data, toml_file)
        except Exception as e:
            ErrorHandler.exception_handler(e, SettingsProvider.class_name)
