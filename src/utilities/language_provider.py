from typing import TYPE_CHECKING

import json
import pathlib

from PyQt6.QtCore import QLocale
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QMenu

from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.ui.dialogs.settings_dialog import SettingsDialog

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.joinpath("languages")


class LanguageProvider:
    class_name = "LanguageProvider"

    @staticmethod
    def get_language_code() -> str | None:
        try:
            return QLocale().name()
        except Exception as e:
            ErrorHandler.exception_handler(e, LanguageProvider.class_name)
            return None

    @staticmethod
    def apply_ui_text(widget: QMainWindow | QWidget, language: str = None) -> bool:
        try:
            if language is None:
                language = LanguageProvider.get_language_code()
            if not language:
                raise ValueError("Load language error.")
            json_text = LanguageProvider.get_text(language, "ui_text")
            if not json_text:
                raise ValueError(f"Load json text error: {json_text}.")
            LanguageProvider.set_ui_text(widget, json_text)
            return True
        except Exception as e:
            ErrorHandler.exception_handler(e, LanguageProvider.class_name)
            return False

    @staticmethod
    def set_ui_text(main_widget: QWidget, json_text: dict[str, dict[str, str]]) -> None:
        try:
            main_name = main_widget.objectName()
            if main_name in json_text:
                widget_text = json_text.get(main_name, "")
                QApplication.setApplicationName(widget_text.get(f"{main_name}Title", "IvalineX"))
                if hasattr(main_widget, "setWindowTitle"):
                    main_widget.setWindowTitle(widget_text.get(f"{main_name}Title", "IvalineX"))
                child_widgets = main_widget.findChildren(QWidget)
                for widget in child_widgets:
                    if widget.objectName() in widget_text:
                        if hasattr(widget, "setText"):
                            widget.setText(widget_text.get(widget.objectName(), "Text"))
                        if hasattr(widget, "setPlaceholderText"):
                            widget.setPlaceholderText(widget_text.get(widget.objectName(), "PlaceholderText"))
                if hasattr(main_widget, "menuBar") and main_widget.menuBar():
                    menu_bar = main_widget.menuBar()
                    for menu in menu_bar.findChildren(QMenu):
                        if menu.objectName() in widget_text:
                            menu.setTitle(widget_text.get(menu.objectName(), "Menu"))
                        for action in menu.actions():
                            if action.objectName() in widget_text:
                                action.setText(widget_text.get(action.objectName(), "Action"))
        except Exception as e:
            ErrorHandler.exception_handler(e, LanguageProvider.class_name)

    @staticmethod
    def apply_settings_dialog_text(dialog: "SettingsDialog", json_text: dict[str, str]) -> None:
        try:
            if not json_text:
                raise ValueError(f"Load json text error: {json_text}.")
            dialog.setWindowTitle(json_text.get(f"{dialog.objectName()}Title", "Settings"))
            for widget, default in [
                (dialog.reset_button, "Reset to default"),
                (dialog.save_button, "Save"),
                (dialog.cancel_button, "Cancel"),
            ]:
                widget.setText(json_text.get(widget.objectName(), default))
            dialog.set_basic_ui_text(
                json_text.get(f"{dialog.basic_groupbox.objectName()}Title", "Basic"),
                json_text.get(dialog.language_label_text.objectName(), "Application language:"),
                json_text.get(dialog.folder_label_text.objectName(), "Folder path:"),
                json_text.get(dialog.folder_edit.objectName(), "Select folder path..."),
                json_text.get(dialog.select_folder_button.objectName(), "Select folder"),
                json_text.get(dialog.history_checkbox.objectName(), "Save history"),
            )
            for widget, default in [
                (dialog.python_tab.init_checkbox, "Ignore __init__.py"),
                (dialog.python_tab.setup_checkbox, "Ignore setup.py"),
                (dialog.python_tab.main_checkbox, "Ignore __main__"),
                (dialog.python_tab.empty_rows_checkbox, "Count empty rows"),
                (dialog.python_tab.comments_checkbox, "Count comments"),
                (dialog.python_tab.ignore_venv_checkbox, "Ignore venv/ .venv/"),
                (dialog.python_tab.ignore_tests_checkbox, "Ignore tests/"),
            ]:
                widget.setText(json_text.get(widget.objectName(), default))
            dialog.set_language_ui_text(
                json_text.get(f"{dialog.language_groupbox.objectName()}Title", "Language")
            )
            for widget, default in [
                (dialog.json_checkbox, "Add JSON / YAML / TOML"),
                (dialog.readme_checkbox, "Count README and documentation"),
                (dialog.ignore_files_checkbox, "Ignore big files (>5 MB)"),
                (dialog.ignore_binary_checkbox, "Ignore binary files"),
            ]:
                widget.setText(json_text.get(widget.objectName(), default))
            dialog.set_common_ui_text(
                json_text.get(f"{dialog.common_groupbox.objectName()}Title", "Common"),
                dialog.json_checkbox.text(),
                dialog.readme_checkbox.text(),
                dialog.ignore_files_checkbox.text(),
                dialog.ignore_binary_checkbox.text(),
            )
        except Exception as e:
            ErrorHandler.exception_handler(e, LanguageProvider.class_name)

    @staticmethod
    def get_dialog_text(language: str, dialog_name: str) -> tuple[dict[str, str], str] | dict[str, str]:
        try:
            json_text = LanguageProvider.get_text(language, "dialog_text")
            if not json_text:
                raise ValueError(f"Load json text error: {json_text}.")
            if dialog_name.startswith("manual"):
                with open(BASE_DIR.joinpath(language, "manual.txt"), "r", encoding="utf-8") as txt_file:
                    return json_text.get(dialog_name, {}), txt_file.read()
            return json_text.get(dialog_name, {})
        except Exception as e:
            ErrorHandler.exception_handler(e, LanguageProvider.class_name)
            if dialog_name.startswith("manual"):
                return {}, ""
            return {}

    @staticmethod
    def get_text(language_code: str | None, file_name: str) -> dict[str, dict[str, str]] | None:
        try:
            json_path = BASE_DIR.joinpath(language_code).joinpath(f"{file_name}.json")
            if not json_path.exists() or json_path.stat().st_size == 0:
                raise FileNotFoundError(f"Text file not found: {json_path}")
            with open(json_path, "r", encoding="utf-8") as json_file:
                json_text = json.load(json_file)
                if json_text:
                    return json_text
            return None
        except Exception as e:
            ErrorHandler.exception_handler(e, LanguageProvider.class_name)
            return None