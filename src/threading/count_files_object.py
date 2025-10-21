import pathlib
import time

from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from src.core.providers.count_provider import CountProvider


# noinspection PyUnresolvedReferences
class CountFilesObject(QObject):
    finished = pyqtSignal(dict)
    error = pyqtSignal(Exception)
    def __init__(self, count_provider: "CountProvider", folder_path: str, toml_data: dict[str, bool]) -> None:
        super().__init__()
        self.setObjectName("countFilesObject")
        self.count_provider = count_provider
        self.folder_path = folder_path
        self.toml_data = toml_data
        self.default_list = []
        self.string_list = []
        self.large_list = []

    def count_files(self) -> None:
        try:
            if not self.toml_data:
                self.error.emit(ValueError("Toml data error"))
                return
            files_dict = self.count_provider.get_items_types(self.folder_path)
            rules = [
                ("code", True),
                ("init", self.toml_data.get("initCheckboxUser", False)),
                ("setup", self.toml_data.get("setupCheckboxUser", False)),
                ("main", self.toml_data.get("mainCheckboxUser", False)),
                ("venv", not self.toml_data.get("ignoreVenvCheckboxUser", True)),
                ("tests", not self.toml_data.get("ignoreTestsCheckboxUser", True)),
                ("config", self.toml_data.get("jsonCheckboxUser", False)),
                ("documentation", self.toml_data.get("readmeCheckboxUser", False)),
                ("binary", not self.toml_data.get("ignoreBinaryCheckboxUser", True)),
            ]
            for key, condition in rules:
                if condition:
                    self.update_lists(files_dict.get(key, []))
            if not self.toml_data.get("ignoreFilesCheckboxUser", True):
                self.large_list.extend(files_dict.get("large", []))
            result = {
                "defaultList": self.default_list,
                "stringList": self.string_list,
                "largeList": self.large_list,
            }
            time.sleep(2)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(e)

    def update_lists(self, files_list: list[pathlib.Path | str]) -> None:
        if files_list:
            string_list = []
            self.default_list.extend(files_list)
            for path in files_list:
                string_path = str(path.relative_to(self.folder_path))
                string_list.append(string_path)
            self.string_list.extend(string_list)