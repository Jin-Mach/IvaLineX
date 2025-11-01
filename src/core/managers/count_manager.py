import pathlib

from typing import TYPE_CHECKING, Type

from PyQt6.QtCore import QThread, QTimer, QElapsedTimer

from src.core.providers.count_provider import CountProvider
from src.core.providers.language_provider import LanguageProvider
from src.core.providers.settings_provider import SettingsProvider
from src.threading.count_files_object import CountFilesObject
from src.threading.count_rows_object import CountRowsObject
from src.ui.dialogs.result_dialog import ResultDialog
from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow
    from src.core.managers.settings_manager import SettingsManager


# noinspection PyAttributeOutsideInit
class CountManager:
    def __init__(self, main_window: "MainWindow") -> None:
        self.class_name = "countManager"
        self.main_window = main_window
        self.count_provider = CountProvider()

    def get_rows_count(self, files_list: list[pathlib.Path]) -> None:
        try:
            self.timer = QElapsedTimer()
            self.timer.start()
            toml_data = SettingsProvider.get_toml_data().get("python_settings", {})
            self.rows_count_object = CountRowsObject(files_list, toml_data, self.count_provider)
            self.rows_count_thread = QThread()
            self.rows_count_object.moveToThread(self.rows_count_thread)
            self.rows_count_thread.started.connect(self.rows_count_object.count_rows)
            self.rows_count_object.finished.connect(self.rows_finished)
            self.rows_count_object.error.connect(self.on_error)
            self.rows_count_object.finished.connect(self.rows_count_thread.quit)
            self.rows_count_thread.finished.connect(self.rows_count_thread.deleteLater)
            self.rows_count_thread.finished.connect(self.rows_count_object.deleteLater)
            self.rows_count_thread.start()
        except Exception as e:
            self.timer = None
            ErrorHandler.exception_handler(e, self.class_name)

    def set_files_list(self, settings_manager: "Type[SettingsManager]") ->  None:
        try:
            folder_path = settings_manager.full_folder_path
            toml_data = SettingsProvider.get_toml_data().get("python_settings", {})
            self.files_count_object = CountFilesObject(self.count_provider, folder_path, toml_data)
            self.files_count_thread = QThread()
            self.files_count_object.moveToThread(self.files_count_thread)
            self.files_count_thread.started.connect(self.files_count_object.count_files)
            self.files_count_object.finished.connect(self.files_finished)
            self.files_count_object.error.connect(self.on_error)
            self.files_count_object.finished.connect(self.files_count_thread.quit)
            self.files_count_thread.finished.connect(self.files_count_thread.deleteLater)
            self.files_count_thread.finished.connect(self.files_count_object.deleteLater)
            self.files_count_thread.start()
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

    def rows_finished(self, count_dict: dict[str, int]) -> None:
        try:
            result_dialog = ResultDialog(self.main_window)
            result_dialog_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language,
                                                                  result_dialog.objectName())
            settings = SettingsProvider.get_toml_data()
            result_dialog.setup_dialog(result_dialog_text.get("resultLabelText", "Done!"),
                                       result_dialog_text.get("codeResultText", "Number of code lines:"),
                                       result_dialog_text.get("emptyResultText", "Number of empty lines:"),
                                       result_dialog_text.get("commentsResultText", "Number of comments:"),
                                       result_dialog_text.get("closeButton", "Close"),
                                       result_dialog_text.get("timeLabelText", "Duration:"),
                                       settings)
            elapsed_ms = self.timer.elapsed()
            seconds = elapsed_ms // 1000
            milliseconds = elapsed_ms % 1000
            minutes = seconds // 60
            seconds = seconds % 60
            duration = f"{minutes:02}:{seconds:02}.{milliseconds:03}"
            result_dialog.on_finished(count_dict, duration)
            QTimer.singleShot(500, result_dialog.show)
        except Exception as e:
            self.timer = None
            ErrorHandler.exception_handler(e, self.class_name)

    def on_error(self, exception: Exception) -> None:
        ErrorHandler.exception_handler(exception, self.class_name)

    def remove_default_item(self, item_text: str) -> None:
        try:
            if not self.default_list:
                raise ValueError("Default list error")
            for path in self.default_list:
                if path.as_posix().endswith(item_text):
                    self.default_list.remove(path)
                    break
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)