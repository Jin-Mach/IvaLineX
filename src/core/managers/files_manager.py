import pathlib
import requests

from src.core.providers.files_provider import FilesProvider
from src.utilities.helpers import Helpers
from src.utilities.logger_provider import get_logger

BASE_URL = "https://raw.githubusercontent.com/Jin-Mach/IvaLineX/main"
BASE_DIR = pathlib.Path(__file__).parents[3]
logger = get_logger()


class FilesManager:
    class_name = "filesManager"

    @staticmethod
    def download_missing_files() -> bool:
        try:
            config_url = f"{BASE_URL}/config"
            language_url = f"{BASE_URL}/languages"
            config_path = BASE_DIR.joinpath("config")
            config_path.mkdir(parents=True, exist_ok=True)
            languages_path = BASE_DIR.joinpath("languages")
            languages_path.mkdir(parents=True, exist_ok=True)
            missing_toml_files = FilesProvider.check_toml_files()
            missing_languages_files = FilesProvider.check_language_files()
            if not Helpers.check_internet_connection():
                return False
            if missing_toml_files:
                for toml_file in missing_toml_files:
                    toml_file_url = f"{config_url}/{toml_file}"
                    toml_file_content = requests.get(toml_file_url, timeout=5).content
                    toml_file_path = config_path.joinpath(toml_file)
                    toml_file_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(toml_file_path, "wb") as file:
                        file.write(toml_file_content)
            if missing_languages_files:
                for language_file in missing_languages_files:
                    language_file_url = f"{language_url}/{language_file}"
                    language_file_content = requests.get(language_file_url, timeout=5).content
                    language_file_path = languages_path.joinpath(language_file)
                    language_file_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(language_file_path, "wb") as file:
                        file.write(language_file_content)
            return True
        except Exception as e:
            logger.error(f"{FilesManager.class_name} error: {e}", exc_info=True)
            return False