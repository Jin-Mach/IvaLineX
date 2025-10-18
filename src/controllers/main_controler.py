import pathlib
from typing import TYPE_CHECKING

from src.core.managers.count_manager import CountManager
from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow


class MainController:
    def __init__(self, main_window: "MainWindow") -> None:
        self.class_name = "mainController"
        self.main_window = main_window
        self.create_connection()

    def create_connection(self) -> None:
        self.main_window.count_button.clicked.connect(lambda: self.start_count(self.main_window.folder_line_input.text()))

    def start_count(self, folder_path: str) -> None:
        try:
            if not folder_path:
                raise NameError("Empty folder path")
            CountManager.get_total_count(folder_path)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)