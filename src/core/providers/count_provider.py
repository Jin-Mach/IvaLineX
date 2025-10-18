import pathlib

from src.utilities.error_handler import ErrorHandler


class CountProvider:
    class_name = "countProvider"

    @staticmethod
    def get_items_types(folder_path: str) -> dict[str, list[str]]:
        try:
            folders = ["venv", ".venv", "tests"]
            checked_files = set()
            types_dict = {"code": [],
                          "init": [],
                          "setup": [],
                          "main": [],
                          "venv": [],
                          "tests":[],
                          "config": [],
                          "documentation": [],
                          "large": [],
                          "binary": []
                          }
            for item in pathlib.Path(folder_path).rglob("*"):
                if item not in checked_files:
                    if ".venv" in item.parts or "venv" in item.parts:
                        continue
                        if item.is_dir() and item.name in folders:
                            for file in item.rglob("*"):
                                if file.is_file():
                                    if item.name in ["test", "tests"]:
                                        types_dict["tests"].append(file)
                                    else:
                                        types_dict["venv"].append(file)
                    if item.is_file():
                        if item.suffix == ".py":
                            if item.name == "__init__.py":
                                types_dict["init"].append(item)
                            elif item.name == "setup.py":
                                types_dict["setup"].append(item)
                            elif item.name == "__main__.py":
                                types_dict["main"].append(item)
                            else:
                                types_dict["code"].append(item)
                        elif item.suffix in [".json", ".yaml", ".yml", ".toml", ".txt"] and item.name != "requirements.txt":
                            types_dict["config"].append(item)
                        elif item.suffix == ".md" or item.name == "LICENSE" or item.name == "requirements.txt":
                            types_dict["documentation"].append(item)
                        elif item.suffix.lower() in [".bin", ".class", ".dll", ".dmg", ".exe", ".o", ".so"]:
                            types_dict["binary"].append(item)
                        if item.stat().st_size > 5 * 1024 * 1024 and item.suffix != ".py":
                            types_dict["large"].append(item)
                    checked_files.add(item)
            return types_dict
        except Exception as e:
            ErrorHandler.exception_handler(e, CountProvider.class_name)
            return {}