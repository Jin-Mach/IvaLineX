from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics

from PyQt6.QtWidgets import QFileDialog, QLineEdit, QWidget

from src.core.managers.language_manager import LanguageManager
from src.core.providers.language_provider import LanguageProvider
from src.utilities.error_handler import ErrorHandler
from src.core.providers.settings_provider import SettingsProvider

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow
    from src.ui.dialogs.settings_dialog import SettingsDialog
    from src.utilities.helpers import Helpers


# noinspection PyUnresolvedReferences
class SettingsManager:
    class_name = "settingsManager"
    full_folder_path = None

    @staticmethod
    def apply_main_window_config(save_history_checkbox) -> bool:
        try:
            toml_data = SettingsProvider.get_toml_data()
            if not toml_data:
                raise ValueError(f"Load toml data error.")
            history_value = toml_data.get("history_settings", {}).get("historyCheckboxUser", True)
            if history_value:
                save_history_checkbox.setChecked(history_value)
            return True
        except Exception as e:
            ErrorHandler.exception_handler(e, SettingsManager.class_name)
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
                            if isinstance(value, dict):
                                selected = value.get("selected", "English")
                                options = value.get("options", [])
                                widget.addItems(options)
                                if selected in options:
                                    widget.setCurrentText(selected)
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
            ErrorHandler.exception_handler(e, SettingsManager.class_name)

    @staticmethod
    def reset_application_settings(main_window: "MainWindow", dialog: "SettingsDialog", helpers: "Helpers") -> None:
        try:
            toml_data = SettingsProvider.get_toml_data()
            if not toml_data:
                raise ValueError("Load toml data error.")
            SettingsProvider.reset_settings(toml_data)
            SettingsProvider.set_toml_data(helpers, toml_data, from_reset=True)
            reset_data = SettingsProvider.get_toml_data()
            new_language = reset_data.get("language_settings", {}).get("languageUser", "en_GB")
            LanguageProvider.usage_language = new_language
            LanguageManager.apply_ui_text(main_window, new_language)
            SettingsManager.apply_main_window_config(main_window.save_history_checkbox)
            dialog.close()
        except Exception as e:
            ErrorHandler.exception_handler(e, SettingsManager.class_name)

    @staticmethod
    def set_folder_path(parent: "MainWindow | SettingsDialog", dialog_title: str, folder_line_edit: QLineEdit) -> None:
        try:
            user_path = ""
            toml_data = SettingsProvider.get_toml_data()
            path_section = toml_data.setdefault("path_settings", {})
            if path_section:
                user_path = path_section["folderEditUser"]
            folder_path = QFileDialog.getExistingDirectory(parent, dialog_title, user_path,
                                                           options=QFileDialog.Option.ShowDirsOnly)
            if folder_path:
                SettingsManager.full_folder_path = folder_path
                metrics = QFontMetrics(folder_line_edit.font())
                short_path = metrics.elidedText(folder_path, Qt.TextElideMode.ElideLeft, folder_line_edit.width())
                folder_line_edit.setText(short_path)
                folder_line_edit.setToolTip(folder_path)
        except Exception as e:
            ErrorHandler.exception_handler(e, SettingsManager.class_name)