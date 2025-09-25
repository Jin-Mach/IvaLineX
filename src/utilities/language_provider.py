import json
import pathlib

from PyQt6.QtCore import QLocale
from PyQt6.QtWidgets import QWidget

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
    def set_ui_text(main_widget: QWidget) -> bool:
        try:
            language = LanguageProvider.get_language_code()
            if not language:
                raise ValueError(f"Load language error.")
            text_json = LanguageProvider.get_ui_text(language)
            if not text_json:
                raise ValueError(f"Load text error.")
            main_name = main_widget.objectName()
            if main_name in text_json:
                widget_text = text_json.get(main_name, "")
                if hasattr(main_widget, "setWindowTitle"):
                    main_widget.setWindowTitle(widget_text.get(f"{main_name}Title", ""))
            return True
        except Exception as e:
            ErrorHandler.exception_handler(e, LanguageProvider.class_name)
            return False

    @staticmethod
    def get_ui_text(language_code: str | None) -> dict[str, str] | None:
        try:
            json_path = BASE_DIR.joinpath(language_code).joinpath("ui_text.json")
            if not json_path.exists() or json_path.stat().st_size == 0:
                raise FileNotFoundError(f"UI text file not found: {json_path}")
            with open(json_path, "r", encoding="utf-8") as json_file:
                json_text = json.load(json_file)
                if json_text:
                    return json_text
            return None
        except Exception as e:
            ErrorHandler.exception_handler(e, LanguageProvider.class_name)
            return None