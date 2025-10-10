from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QApplication

from src.ui.dialogs.about_dialog import AboutDialog
from src.ui.dialogs.manual_dialog import ManualDialog
from src.ui.dialogs.question_dialog import QuestionDialog
from src.ui.dialogs.settings_dialog import SettingsDialog
from src.utilities.error_handler import ErrorHandler
from src.core.managers.language_manager import LanguageManager
from src.core.providers.language_provider import LanguageProvider
from src.core.managers.settings_manager import SettingsManager
from src.core.providers.settings_provider import SettingsProvider
from src.utilities.helpers import Helpers

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow
    from src.ui.widgets.menu_bar import MenuBar


class DialogsController:
    def __init__(self, main_window: "MainWindow", menu_bar: "MenuBar") -> None:
        self.class_name = "dialogsController"
        self.main_window = main_window
        self.menu_bar = menu_bar
        self.settings_provider = SettingsProvider()
        self.settings_manager = SettingsManager()
        self.create_connection()

    def create_connection(self) -> None:
        self.menu_bar.settings_action.triggered.connect(self.show_settings_dialog)
        self.menu_bar.close_app_action.triggered.connect(self.show_close_app_dialog)
        self.menu_bar.manual_action.triggered.connect(self.show_manual_dialog)
        self.menu_bar.about_action.triggered.connect(self.show_about_dialog)

    def set_folder_path(self) -> None:
        try:
            settings_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, "getDirDialog")
            if not settings_text:
                raise ValueError("Load json text error.")
            self.settings_manager.set_folder_path(self.main_window, settings_text.get("folderDialogTitle", "Select default folder"),
                                                   self.main_window.folder_line_input)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_settings_dialog(self) -> None:
        try:
            dialog = SettingsDialog(self.main_window)
            self.settings_manager.apply_settings_dialog_config(dialog)
            settings_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, dialog.objectName())
            if not settings_text:
                raise ValueError("Load json text error.")
            LanguageManager.apply_settings_dialog_text(dialog, settings_text)
            dialog.folder_button_clicked.connect(lambda: self.settings_manager.set_folder_path(dialog,
                                                                         settings_text.get("folderDialogTitle", "Select default folder"),
                                                                         dialog.folder_edit))
            if dialog.exec() == dialog.DialogCode.Accepted:
                settings_data = dialog.get_settings_data()
                if settings_data:
                    helper = Helpers()
                    SettingsProvider.set_toml_data(helper, settings_data)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_close_app_dialog(self) -> None:
        try:
            dialog = QuestionDialog(self.main_window)
            question_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, dialog.objectName())
            if not question_text:
                raise ValueError("Load json text error.")
            dialog.set_ui_text(question_text.get("closeAppQuestion", "Close application?"),
                               question_text.get("questionAcceptButton", "Yes"),
                               question_text.get("questionCancelButton", "No"))
            if dialog.exec() == dialog.DialogCode.Accepted:
                QApplication.quit()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_manual_dialog(self) -> None:
        try:
            dialog = ManualDialog(self.main_window)
            manual_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, dialog.objectName())
            if not manual_text:
                raise ValueError("Load json text error.")
            dialog.set_ui_text(manual_text)
            dialog.exec()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_about_dialog(self) -> None:
        try:
            dialog = AboutDialog(self.main_window)
            about_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, dialog.objectName())
            if not about_text:
                raise ValueError("Load json text error.")
            dialog.set_ui_text(about_text.get(f"{dialog.objectName()}Title", "About application"),
                                about_text.get(dialog.about_label_text.objectName(), "<b>IvalineX</b><br>autor: Jin-Mach<br>verze: 1.0."),
                                about_text.get(dialog.close_button.objectName(), "Close"))
            dialog.exec()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)