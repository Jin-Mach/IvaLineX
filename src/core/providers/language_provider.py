from typing import TYPE_CHECKING

import json
import pathlib

from PyQt6.QtCore import QLocale

from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    pass

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent.joinpath("languages")


class LanguageProvider:
    class_name = "LanguageProvider"
    usage_language = None

    @staticmethod
    def get_language_code() -> str | None:
        try:
            return QLocale().name()
        except Exception as e:
            ErrorHandler.exception_handler(e, LanguageProvider.class_name)
            return None

    @staticmethod
    def get_dialog_text(language: str, dialog_name: str) -> tuple[dict[str, str], str] | dict[str, str]:
        try:
            json_text = LanguageProvider.get_text(language, "dialog_text")
            if not json_text:
                raise ValueError("Load json text error.")
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