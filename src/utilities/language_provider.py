import json
import pathlib

from PyQt6.QtCore import QLocale
from PyQt6.QtWidgets import QWidget, QMainWindow

from src.utilities.error_handler import ErrorHandler

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
                if hasattr(main_widget, "setWindowTitle"):
                    main_widget.setWindowTitle(widget_text.get(f"{main_name}Title", ""))
                child_widgets = main_widget.findChildren(QWidget)
                for widget in child_widgets:
                    if widget.objectName() in widget_text:
                        if hasattr(widget, "setText"):
                            widget.setText(widget_text.get(f"{widget.objectName()}", ""))
                        if hasattr(widget, "setPlaceholderText"):
                            widget.setPlaceholderText(widget_text.get(f"{widget.objectName()}", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, LanguageProvider.class_name)

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