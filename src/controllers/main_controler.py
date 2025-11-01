import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import QModelIndex

from src.core.providers.language_provider import LanguageProvider
from src.core.providers.settings_provider import SettingsProvider
from src.ui.dialogs.progress_dialog import ProgressDialog
from src.ui.dialogs.question_dialog import QuestionDialog
from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow
    from src.controllers.dialogs_controler import DialogsController
    from src.core.managers.count_manager import CountManager


class MainController:
    def __init__(self, main_window: "MainWindow", dialog_controller: "DialogsController", count_manager: "CountManager") -> None:
        self.class_name = "mainController"
        self.main_window = main_window
        self.dialog_controller = dialog_controller
        self.count_manager = count_manager
        self.create_connection()

    def create_connection(self) -> None:
        self.main_window.folder_button.clicked.connect(self.dialog_controller.set_folder_path)
        self.main_window.folder_list_view.doubleClicked.connect(self.remove_selected_item)
        self.main_window.count_button.clicked.connect(lambda: self.start_count(self.dialog_controller.project_path))

    def start_count(self, folder_path: pathlib.Path) -> None:
        try:
            if not folder_path or not folder_path.exists():
                raise NameError("Empty folder path")
            if not self.count_manager.default_list:
                raise ValueError("Default list error")
            progress_dialog = ProgressDialog(True, self.main_window)
            dialog_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language,
                                                           progress_dialog.objectName())
            progress_dialog.setup_dialog(dialog_text.get("labelTextRows", "Count rows..."), 100,
                                         dialog_text.get("onFinished", "Completed"))
            progress_dialog.show()
            self.count_manager.get_rows_count(self.count_manager.default_list, SettingsProvider)
            self.count_manager.rows_count_object.progress.connect(progress_dialog.progress_bar.setValue)
            self.count_manager.rows_count_thread.finished.connect(progress_dialog.on_finished)
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
                    self.count_manager.remove_default_item(item_text)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)