import pathlib

from src.utilities.error_handler import ErrorHandler


class CountProvider:
    class_name = "countProvider"

    @staticmethod
    def get_items_types(folder_path: str) -> dict[str, list[pathlib.Path]]:
        try:
            folders = ["venv", ".venv", "test", "tests"]
            types_dict = {"code": [], "init": [], "setup": [], "main": [], "venv": [], "tests": [], "config": [],
                          "documentation": [], "large": [], "binary": []}
            checked_files = set()
            for item in pathlib.Path(folder_path).rglob("*"):
                if "__pycache__" in str(item):
                    continue
                if item in checked_files:
                    continue
                if item.is_dir() and item.name in folders:
                    for file in item.rglob("*"):
                        if file.is_file() and file.stat().st_size > 0 and "__pycache__" not in str(file):
                            if item.name in ["test", "tests"]:
                                types_dict["tests"].append(file)
                            else:
                                types_dict["venv"].append(file)
                            checked_files.add(file)
                elif item.is_file() and item.stat().st_size > 0:
                    if item.suffix == ".py":
                        if item.name == "__init__.py":
                            types_dict["init"].append(item)
                        elif item.name == "setup.py":
                            types_dict["setup"].append(item)
                        elif item.name == "__main__.py":
                            types_dict["main"].append(item)
                        else:
                            types_dict["code"].append(item)
                    elif item.suffix.lower() in [".json", ".yaml", ".yml", ".toml"] and item.name.lower() != "requirements.txt":
                        types_dict["config"].append(item)
                    elif item.suffix.lower() == ".md" or item.name.lower() in ["license", "requirements.txt"]:
                        types_dict["documentation"].append(item)
                    elif item.suffix.lower() in [".bin", ".class", ".dll", ".dmg", ".exe", ".o", ".so"]:
                        types_dict["binary"].append(item)
                    if item.stat().st_size > 5 * 1024 * 1024 and item.suffix != ".py":
                        types_dict["large"].append(item)
                    checked_files.add(item)
            for key in types_dict.keys():
                types_dict[key].sort()
            return types_dict
        except Exception as e:
            ErrorHandler.exception_handler(e, CountProvider.class_name)
            return {}

    @staticmethod
    def count_project_rows(files_list: list[pathlib.Path]) -> dict[str, int]:
        try:
            count_result = {
                "code": 0,
                "empty": 0,
                "comments": 0
            }
            for project_file in files_list:
                if not project_file.exists():
                    raise FileNotFoundError("Count file doesnt exists")
                if project_file.suffix == ".py":
                    file_count = CountProvider.count_python_file(project_file)
                    count_result["code"] += file_count["code"]
                    count_result["empty"] += file_count["empty"]
                    count_result["comments"] += file_count["comments"]
                else:
                    file_count = CountProvider.count_other_file(project_file)
                    count_result["code"] += file_count["code"]
                    count_result["empty"] += file_count["empty"]
            return count_result
        except Exception as e:
            ErrorHandler.exception_handler(e, CountProvider.class_name)
            return {}

    @staticmethod
    def count_python_file(file: pathlib.Path) -> dict[str, int]:
        file_count = {"code": 0, "empty": 0, "comments": 0}
        in_docstring = False
        docstring_char = None
        with open(file, "r", encoding="utf-8") as file_content:
            for line in file_content:
                stripped = line.strip()
                if in_docstring:
                    file_count["comments"] += 1
                    if stripped.endswith(docstring_char):
                        in_docstring = False
                        docstring_char = None
                    continue
                if ((stripped.startswith('"""') or stripped.startswith("'''")) and (stripped.endswith('"""')
                    or stripped.endswith("'''")) and len(stripped) > 6):
                    file_count["comments"] += 1
                    continue
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    file_count["comments"] += 1
                    docstring_char = stripped[:3]
                    if not (stripped.endswith(docstring_char) and len(stripped) > 3):
                        in_docstring = True
                        continue
                if stripped == "":
                    file_count["empty"] += 1
                    continue
                if stripped.startswith("#"):
                    file_count["comments"] += 1
                    continue
                file_count["code"] += 1
        return file_count

    @staticmethod
    def count_other_file(file: pathlib.Path) -> dict[str, int]:
        file_count = {"code": 0, "empty": 0}
        with open(file, "r", encoding="utf-8") as file:
            content = file.read()
            for row in content.strip().split("\n"):
                if row.strip() != "":
                    file_count["code"] += 1
                else:
                    file_count["empty"] += 1
        return file_count