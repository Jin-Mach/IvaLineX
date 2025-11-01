import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from src.core.providers.count_provider import CountProvider


# noinspection PyUnresolvedReferences
class CountRowsObject(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(Exception)
    def __init__(self, rows_list: list[pathlib.Path], toml_data: dict[str, bool], count_provider: "CountProvider") -> None:
        super().__init__()
        self.setObjectName("countRowsObject")
        self.rows_list = rows_list
        self.toml_data = toml_data
        self.count_provider = count_provider
        self.code_count = 0
        self.empty_count = 0
        self.comments_count = 0

    def count_rows(self) -> None:
        try:
            if not self.toml_data:
                self.error.emit(ValueError("Toml data error"))
                return
            result = {"code": 0, "empty": 0, "comments": 0}
            files_count = len(self.rows_list)
            for index, file in enumerate(self.rows_list):
                file_result = self.count_provider.count_project_rows(file)
                self.code_count += file_result.get("code", 0)
                if self.toml_data.get("emptyRowsCheckboxUser", False):
                    self.empty_count += file_result.get("empty", 0)
                if self.toml_data.get("commentsCheckboxUser", False):
                    self.comments_count += file_result.get("comments", 0)
                progress = int(((index + 1) / files_count) * 100)
                self.progress.emit(progress)
            result["code"] = self.code_count
            result["empty"] = self.empty_count
            result["comments"] = self.comments_count
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(e)