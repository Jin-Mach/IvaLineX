import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import QThread

from src.core.providers.count_provider import CountProvider
from src.threading.count_files_object import CountFilesObject
from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow
    from src.core.managers.settings_manager import SettingsManager
    from src.core.providers.settings_provider import SettingsProvider


class CountManager:
    def __init__(self, main_window: "MainWindow") -> None:
        self.class_name = "countManager"
        self.main_window = main_window

    @staticmethod
    def get_total_count(self, folder_path: str, counted_files: dict[str, list[pathlib.Path]]):
        try:
            counted_files = counted_files
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def set_files_list(self, settings_manager: "SettingsManager", settings_provider: "SettingsProvider") ->  None:
        try:
            folder_path = settings_manager.full_folder_path
            count_provider = CountProvider()
            toml_data = settings_provider.get_toml_data().get("python_settings", {})
            self.count_object = CountFilesObject(count_provider, folder_path, toml_data)
            self.count_thread = QThread()
            self.count_object.moveToThread(self.count_thread)
            self.count_thread.started.connect(self.count_object.count_files)
            self.count_object.finished.connect(self.files_finished)
            self.count_object.error.connect(self.on_error)
            self.count_object.finished.connect(self.count_thread.quit)
            self.count_thread.finished.connect(self.count_thread.deleteLater)
            self.count_thread.finished.connect(self.count_object.deleteLater)
            self.count_thread.start()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)


    def files_finished(self, files_dict: dict[str, list[pathlib.Path | str]]) -> None:
        try:
            self.default_list = files_dict.get("defaultList", [])
            self.string_list = files_dict.get("stringList", [])
            self.large_list = files_dict.get("largeList", [])
            if not self.string_list:
                raise ProcessLookupError("Default list error")
            self.main_window.folder_list_view.update_data(self.string_list)
            self.main_window.files_count_label.setText(str(len(self.string_list)))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def on_error(self, exception: Exception) -> None:
        ErrorHandler.exception_handler(exception, self.class_name)