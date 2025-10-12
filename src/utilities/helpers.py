import json
import pathlib
import requests

from src.core.providers.settings_provider import SettingsProvider
from src.utilities.error_handler import ErrorHandler


class Helpers:
    class_name = "helpers"

    @staticmethod
    def get_exception_text(exception: Exception) -> str:
        error_text = "Unknown error"
        toml_data= SettingsProvider.get_toml_data()
        if toml_data:
            language = toml_data.get("language_settings", {}).get("languageUser", None)
            if not language:
                language = "en_GB"
            error_path =pathlib.Path(__file__).parents[2].joinpath("languages", language, "error_text.json")
            if error_path.exists() and error_path.stat().st_size > 0:
                with open(error_path, "r", encoding="utf-8") as error_file:
                    try:
                        error_data = json.load(error_file)
                    except json.JSONDecodeError:
                        error_data = {}
                    if error_data:
                        error_text = error_data.get(exception.__class__.__name__, "Unknown error")
        return error_text

    @staticmethod
    def get_language_code(language_name: str) -> str:
        try:
            language_code = "en_GB"
            map_dir = pathlib.Path(__file__).parents[2].joinpath("languages", "language_map.json")
            if map_dir.exists() and map_dir.stat().st_size > 0:
                with open(map_dir, "r", encoding="utf-8") as map_file:
                        language_map = json.load(map_file)
                if language_map:
                    language_code = language_map.get(language_name, "en_GB")
            return language_code
        except Exception as e:
            ErrorHandler.exception_handler(e, Helpers.class_name)
            return "en_GB"

    @staticmethod
    def check_internet_connection() -> bool:
        request = requests.head("https://github.com", timeout=3)
        return request.ok

    @staticmethod
    def validate_project_name(project_name: str, load: bool) -> str:
        try:
            if load:
                return project_name.replace("_", " ")
            return f"{project_name.replace(" ", "_")}.json"
        except Exception as e:
            ErrorHandler.exception_handler(e, Helpers.class_name)
            return ""