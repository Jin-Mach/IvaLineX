import json
import pathlib

from src.utilities.settings_provider import SettingsProvider


class HelpersProvider:
    class_name = "helpersProvider"

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