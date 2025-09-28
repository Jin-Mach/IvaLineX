from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QApplication

from src.ui.dialogs.about_dialog import AboutDialog
from src.ui.dialogs.manual_dialog import ManualDialog
from src.ui.dialogs.question_dialog import QuestionDialog
from src.ui.dialogs.settings_dialog import SettingsDialog
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow
    from src.ui.widgets.menu_bar import MenuBar


class DialogsController:
    def __init__(self, main_window: "MainWindow", menu_bar: "MenuBar") -> None:
        self.class_name = "dialogsController"
        self.main_window = main_window
        self.menu_bar = menu_bar
        self.create_connection()

    def create_connection(self) -> None:
        self.menu_bar.settings_action.triggered.connect(self.show_settings_dialog)
        self.menu_bar.close_app_action.triggered.connect(self.show_close_app_dialog)
        self.menu_bar.manual_action.triggered.connect(self.show_manual_dialog)
        self.menu_bar.about_action.triggered.connect(self.show_about_dialog)

    def show_settings_dialog(self) -> None:
        try:
            dialog = SettingsDialog(self.main_window)
            settings_text = LanguageProvider.set_dialog_text("cs_CZ", dialog.objectName())
            for widget, key, default in [
                (dialog.reset_button, dialog.reset_button.objectName(), "Reset to default"),
                (dialog.save_button, dialog.save_button.objectName(), "Save"),
                (dialog.cancel_button, dialog.cancel_button.objectName(), "Cancel"),
            ]:
                widget.setText(settings_text.get(key, default))
            dialog.set_basic_ui_text(
                settings_text.get(f"{dialog.basic_groupbox.objectName()}Title", "Basic"),
                settings_text.get(dialog.folder_label_text.objectName(), "Folder path:"),
                settings_text.get(dialog.folder_edit.objectName(), "Select folder path..."),
                settings_text.get(dialog.select_folder_button.objectName(), "Select folder"),
                settings_text.get(dialog.history_checkbox.objectName(), "Save history"),
            )
            for widget, default in [
                (dialog.python_tab.init_checkbox, "Ignore __init__.py"),
                (dialog.python_tab.setup_checkbox, "Ignore setup.py"),
                (dialog.python_tab.main_checkbox, "Ignore __main__"),
                (dialog.python_tab.empty_rows_checkbox, "Count empty rows"),
                (dialog.python_tab.comments_checkbox, "Count comments"),
                (dialog.python_tab.ignore_venv_checkbox, "Ignore venv/ .venv/"),
                (dialog.python_tab.ignore_tests_checkbox, "Ignore tests/"),
            ]:
                widget.setText(settings_text.get(widget.objectName(), default))
            dialog.set_language_ui_text(
                settings_text.get(f"{dialog.language_groupbox.objectName()}Title", "Language")
            )
            for widget, default in [
                (dialog.json_checkbox, "Add JSON / YAML / TOML"),
                (dialog.readme_checkbox, "Count README and documentation"),
                (dialog.ignore_files_checkbox, "Ignore big files (>5 MB)"),
                (dialog.ignore_binary_checkbox, "Ignore binary files"),
            ]:
                widget.setText(settings_text.get(widget.objectName(), default))
            dialog.set_common_ui_text(
                settings_text.get(f"{dialog.common_groupbox.objectName()}Title", "Common"),
                dialog.json_checkbox.text(),
                dialog.readme_checkbox.text(),
                dialog.ignore_files_checkbox.text(),
                dialog.ignore_binary_checkbox.text(),
            )
            dialog.exec()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_close_app_dialog(self) -> None:
        try:
            dialog = QuestionDialog(self.main_window)
            question_text = LanguageProvider.set_dialog_text("cs_CZ", dialog.objectName())
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
            manual_text = LanguageProvider.set_dialog_text("cs_CZ", dialog.objectName())
            if manual_text:
                dialog.set_ui_text(manual_text)
            dialog.exec()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_about_dialog(self) -> None:
        try:
            dialog = AboutDialog(self.main_window)
            about_text = LanguageProvider.set_dialog_text("cs_CZ", dialog.objectName())
            if about_text:
                dialog.set_ui_text(about_text.get(f"{dialog.objectName()}Title", "About application"),
                                   about_text.get(dialog.about_label_text.objectName(), "<b>IvalineX</b><br>autor: Jin-Mach<br>verze: 1.0."),
                                   about_text.get(dialog.close_button.objectName(), "Close"))
            dialog.exec()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)
