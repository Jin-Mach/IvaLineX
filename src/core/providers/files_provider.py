import pathlib

from src.utilities.logger_provider import get_logger

BASE_DIR = pathlib.Path(__file__).parents[3]
logger = get_logger()


class FilesProvider:
    class_name = "filesProvider"

    @staticmethod
    def check_toml_files() -> list[str]:
        try:
            toml_path = BASE_DIR.joinpath("config")
            toml_path.mkdir(parents=True, exist_ok=True)
            required_files = ["app_settings.toml"]
            missing_files = []
            for file in required_files:
                if not toml_path.joinpath(file).exists():
                    missing_files.append(file)
            return missing_files
        except Exception as e:
            logger.error(f"{FilesProvider.class_name} error: {e}", exc_info=True)
            return []

    @staticmethod
    def check_language_files() -> list[str]:
        try:
            language_path = BASE_DIR.joinpath("languages")
            language_path.mkdir(parents=True, exist_ok=True)
            required_language_folders = ["cs_CZ", "en_GB"]
            required_language_files = ["dialog_text.json", "error_text.json", "manual.txt", "ui_text.json"]
            required_files = ["language_map.json"]
            missing_files = []
            for folder in required_language_folders:
                language_path.joinpath(folder).mkdir(parents=True, exist_ok=True)
            for language_folder in language_path.iterdir():
                if language_folder.is_dir():
                    for file in required_language_files:
                        if not language_folder.joinpath(file).exists():
                            missing_files.append(language_folder.joinpath(file).relative_to(language_path))
            for file in required_files:
                if not language_path.joinpath(file).exists():
                    missing_files.append(file)
            return missing_files
        except Exception as e:
            logger.error(f"{FilesProvider.class_name} error: {e}", exc_info=True)
            return []