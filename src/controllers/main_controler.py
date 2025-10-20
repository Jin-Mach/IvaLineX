from typing import TYPE_CHECKING

from PyQt6.QtCore import QModelIndex

from src.core.providers.language_provider import LanguageProvider
from src.ui.dialogs.question_dialog import QuestionDialog
from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow
    from src.core.managers.count_manager import CountManager


class MainController:
    def __init__(self, main_window: "MainWindow", count_manager: "CountManager") -> None:
        self.class_name = "mainController"
        self.main_window = main_window
        self.count_manager = count_manager
        self.create_connection()

    def create_connection(self) -> None:
        self.main_window.folder_list_view.doubleClicked.connect(self.remove_selected_item)
        self.main_window.count_button.clicked.connect(lambda: self.start_count(self.main_window.folder_line_input.text()))

    def start_count(self, folder_path: str) -> None:
        try:
            if not folder_path:
                raise NameError("Empty folder path")
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def remove_selected_item(self, index: QModelIndex) -> None:
        try:
            dialog = QuestionDialog(self.main_window)
            question_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, dialog.objectName())
            if not question_text:
                raise ValueError("load json text error")
            question = question_text.get("deleteItem", "Delete item?")
            item_text = index.model().data(index)
            dialog.set_ui_text(
                f"{question}\n{item_text}",
                question_text.get("questionAcceptButton", "Yes"),
                question_text.get("questionCancelButton", "No")
            )
            if dialog.exec() == dialog.DialogCode.Accepted:
                if index.isValid():
                    self.main_window.folder_list_view.remove_item(index)
                    self.main_window.files_count_label.setText(str(self.main_window.folder_list_view.model.rowCount()))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)