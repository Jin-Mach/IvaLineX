from typing import TYPE_CHECKING, Any, Callable

import pathlib
import tomllib
import tomli_w

from src.utilities.error_handler import ErrorHandler
from src.core.providers.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.utilities.helpers import Helpers

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent.joinpath("config", "app_settings.toml")


# noinspection PyUnresolvedReferences
class SettingsProvider:
    class_name = "settingsProvider"

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
                raise ValueError("Load toml data error.")
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

    @staticmethod
    def set_toml_data(helpers: "Helpers", settings_data: dict[str, dict[str, Any]]) -> None:
        try:
            toml_data = SettingsProvider.get_toml_data()
            if not toml_data:
                raise ValueError("Load toml data error.")
            for section, section_dict in settings_data.items():
                for key, value in section_dict.items():
                    if key == "languageUser":
                        language_code = helpers.get_language_code(value)
                        toml_data[section][key] = language_code
                        if "languageComboboxUser" in toml_data.get(section, {}):
                            toml_data[section]["languageComboboxUser"]["selected"] = value
                    else:
                        toml_data[section][key] = value
            with open(BASE_DIR, "wb") as new_toml:
                tomli_w.dump(toml_data, new_toml)
        except Exception as e:
            ErrorHandler.exception_handler(e, SettingsProvider.class_name)