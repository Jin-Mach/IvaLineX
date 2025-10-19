import pathlib

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

    def count_files(self) -> None:
        try:
            result = {
                "defaultList": [],
                "stringList": [],
                "largeList": []
            }
            self.default_list = []
            self.string_list = []
            self.large_list = []
            files_dict = self.count_provider.get_items_types(self.folder_path)
            if not self.toml_data:
                self.error.emit(ValueError("Toml data error"))
                return
            self.update_lists(files_dict.get("code", []))
            if self.toml_data.get("initCheckboxUser", False):
                self.update_lists(files_dict.get("init", []))
            if self.toml_data.get("setupCheckboxUser", False):
                self.update_lists(files_dict.get("setup", []))
            if self.toml_data.get("mainCheckboxUser", False):
                self.update_lists(files_dict.get("main", []))
            if not self.toml_data.get("ignoreVenvCheckboxUser", True):
                self.update_lists(files_dict.get("venv", []))
            if not self.toml_data.get("ignoreTestsCheckboxUser", True):
                self.update_lists(files_dict.get("tests", []))
            if self.toml_data.get("jsonCheckboxUser", False):
                self.update_lists(files_dict.get("config", []))
            if self.toml_data.get("readmeCheckboxUser", False):
                self.update_lists(files_dict.get("documentation", []))
            if not self.toml_data.get("ignoreFilesCheckboxUser", True):
                self.large_list.extend(files_dict.get("large", []))
            if not self.toml_data.get("ignoreBinaryCheckboxUser", True):
                self.update_lists(files_dict.get("binary", []))
            result["defaultList"] = self.default_list
            result["stringList"] = self.string_list
            result["largeList"] = self.large_list
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(e)

    def update_lists(self, files_list: list[pathlib.Path]) -> None:
        if files_list:
            string_list = []
            self.default_list.extend(files_list)
            for path in files_list:
                string_path = str(path.relative_to(self.folder_path))
                string_list.append(string_path)
            self.string_list.extend(string_list)
