import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox

from src.core.managers.projects_manager import ProjectsManager
from src.core.providers.projects_provider import ProjectsProvider
from src.ui.dialogs.about_dialog import AboutDialog
from src.ui.dialogs.info_messagebox import InfoMessageBox
from src.ui.dialogs.manual_dialog import ManualDialog
from src.ui.dialogs.new_project_dialog import NewProjectDialog
from src.ui.dialogs.progress_dialog import ProgressDialog
from src.ui.dialogs.question_dialog import QuestionDialog
from src.ui.dialogs.select_project_dialog import SelectProjectDialog
from src.ui.dialogs.settings_dialog import SettingsDialog
from src.ui.dialogs.statistics_dialog import StatisticsDialog
from src.utilities.error_handler import ErrorHandler
from src.core.managers.language_manager import LanguageManager
from src.core.providers.language_provider import LanguageProvider
from src.core.managers.settings_manager import SettingsManager
from src.core.providers.settings_provider import SettingsProvider
from src.utilities.helpers import Helpers

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow
    from src.ui.widgets.menu_bar import MenuBar
    from src.core.managers.count_manager import CountManager


# noinspection PyTypeChecker
class DialogsController:
    def __init__(self, main_window: "MainWindow", menu_bar: "MenuBar", count_manager: "CountManager") -> None:
        self.class_name = "dialogsController"
        self.main_window = main_window
        self.menu_bar = menu_bar
        self.count_manager = count_manager
        self.create_connection()

    def create_connection(self) -> None:
        self.menu_bar.new_project_action.triggered.connect(self.show_new_project_dialog)
        self.menu_bar.open_project_action.triggered.connect(self.show_select_project_dialog)
        self.menu_bar.close_project_action.triggered.connect(self.show_close_project_dialog)
        self.menu_bar.delete_project_action.triggered.connect(self.show_delete_project_dialog)
        self.menu_bar.settings_action.triggered.connect(self.show_settings_dialog)
        self.menu_bar.statistics_action.triggered.connect(self.show_statistics_dialog)
        self.menu_bar.close_app_action.triggered.connect(self.show_close_app_dialog)
        self.menu_bar.manual_action.triggered.connect(self.show_manual_dialog)
        self.menu_bar.about_action.triggered.connect(self.show_about_dialog)

    def show_new_project_dialog(self) -> None:
        try:
            dialog = NewProjectDialog(self.main_window)
            new_project_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, dialog.objectName())
            if not new_project_text:
                raise ValueError("Load json text error.")
            LanguageManager.apply_new_project_dialog_text(dialog, new_project_text)
            if dialog.exec() == dialog.DialogCode.Accepted:
                current_time = QDateTime().currentDateTime().toString(Qt.DateFormat.ISODate)
                if ProjectsManager.create_project_file(self.main_window, dialog.project_name_edit.text().strip(), current_time):
                    ProjectsManager.set_application_to_project(self.main_window, dialog.project_name_edit.text().strip())
                    ProjectsManager.close_project_ui(self.main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_select_project_dialog(self) -> None:
        try:
            dialog = SelectProjectDialog(self.main_window)
            select_project_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, dialog.objectName())
            if not select_project_text:
                raise ValueError("Load json text error")
            LanguageManager.apply_select_project_dialog_text(dialog, select_project_text)
            if ProjectsManager.set_selected_project(self.main_window, dialog.projects_combobox):
                if dialog.exec() == dialog.DialogCode.Accepted:
                    ProjectsManager.set_application_to_project(self.main_window, dialog.projects_combobox.currentText())
                    if ProjectsProvider.project_path:
                        self.show_progress_dialog(self.main_window)
                    else:
                        self.count_manager.default_list = []
                        ProjectsManager.close_project_ui(self.main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_close_project_dialog(self) -> None:
        try:
            if not self.main_window.project_name_label.text():
                return
            dialog = QuestionDialog(self.main_window)
            question_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, dialog.objectName())
            if not question_text:
                raise ValueError("Load json text error.")
            dialog.set_ui_text(
                f"<b>{self.main_window.project_name_label.text()}</b><br>{question_text.get("closeProject", "Close project?")}",
                question_text.get("questionAcceptButton", "Yes"),
                question_text.get("questionCancelButton", "No")
            )
            if dialog.exec() == dialog.DialogCode.Accepted:
                self.main_window.project_name_label.setText("")
                ProjectsManager.close_project_ui(self.main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_delete_project_dialog(self) -> None:
        try:
            dialog = SelectProjectDialog(self.main_window)
            select_project_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language,
                                                                   dialog.objectName())
            if not select_project_text:
                raise ValueError("Load json text error")
            LanguageManager.apply_select_project_dialog_text(dialog, select_project_text)
            if ProjectsManager.set_selected_project(self.main_window, dialog.projects_combobox):
                if dialog.exec() == dialog.DialogCode.Accepted:
                    if dialog.projects_combobox.currentText() != self.main_window.project_name_label.text():
                        ProjectsManager.delete_selected_project(self.main_window, dialog.projects_combobox.currentText())
                    else:
                        question_dialog = QuestionDialog(self.main_window)
                        question_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, question_dialog.objectName())
                        if not question_text:
                            raise ValueError("Load json text error.")
                        question_dialog.set_ui_text(
                            question_text.get("deleteProject", "Delete project?"),
                            question_text.get("questionAcceptButton", "Yes"),
                            question_text.get("questionCancelButton", "No")
                        )
                        if question_dialog.exec() == question_dialog.DialogCode.Accepted:
                            ProjectsManager.delete_selected_project(self.main_window, dialog.projects_combobox.currentText())
                    messagebox = InfoMessageBox(self.main_window)
                    messagebox_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, messagebox.objectName())
                    messagebox.set_ui_text(
                        messagebox_text.get("projectDeleted", "Project deleted"),
                        QMessageBox.Icon.Information,
                        messagebox_text.get("closeButton", "Close"))
                    messagebox.exec()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def set_folder_path(self) -> None:
        try:
            settings_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, "getDirDialog")
            if not settings_text:
                raise ValueError("Load json text error.")
            folder_path = SettingsManager.set_folder_path(self.main_window, settings_text.get("folderDialogTitle", "Select default folder"),
                                                   self.main_window.folder_line_input)
            if folder_path:
                ProjectsProvider.project_path = pathlib.Path(folder_path)
                self.show_progress_dialog(self.main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_settings_dialog(self) -> None:
        try:
            dialog = SettingsDialog(self.main_window)
            SettingsManager.apply_settings_dialog_config(dialog)
            settings_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, dialog.objectName())
            if not settings_text:
                raise ValueError("Load json text error.")
            LanguageManager.apply_settings_dialog_text(dialog, settings_text)
            dialog.folder_button_clicked.connect(lambda: SettingsManager.set_folder_path(dialog,
                                                                         settings_text.get("folderDialogTitle", "Select default folder"),
                                                                         dialog.folder_edit))
            dialog.reset_button.clicked.connect(lambda: self.check_reset_settings(dialog))
            if dialog.exec() == dialog.DialogCode.Accepted:
                settings_data = dialog.get_settings_data()
                if settings_data:
                    helper = Helpers()
                    SettingsProvider.set_toml_data(helper, settings_data)
                    reset_data = SettingsProvider.get_toml_data()
                    new_language = reset_data.get("language_settings", {}).get("languageUser", "en_GB")
                    LanguageProvider.usage_language = new_language
                    LanguageManager.apply_ui_text(self.main_window, LanguageProvider.usage_language)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_statistics_dialog(self) -> None:
        try:
            statistics_dialog = StatisticsDialog(self.main_window)
            statistics_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, statistics_dialog.objectName())
            if not statistics_text:
                raise ValueError("Load json text error.")
            self.projects_data = ProjectsManager.get_statistics_data()
            LanguageManager.apply_statistics_dialog_text(statistics_dialog, list(self.projects_data.keys()), statistics_text)
            statistics_dialog.project_combobox.currentIndexChanged.connect(
                lambda index: self.set_statistics_data(statistics_dialog, index,
                                                       f"{statistics_text.get("totalText", "total")}",
                                                       f"{statistics_text.get("codeLegendText", "code")}",
                                                       f"{statistics_text.get("emptyLegendText", "empty")}",
                                                        f"{statistics_text.get("commentsLegendText", "comments")}"))
            statistics_dialog.exec()
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

    def check_reset_settings(self, dialog: SettingsDialog) -> None:
        try:
            question_dialog = QuestionDialog(dialog)
            question_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language, question_dialog.objectName())
            if not question_text:
                raise ValueError("Load json text error.")
            question_dialog.set_ui_text(
                question_text.get("resetSettings", "Reset application settings?"),
                question_text.get("questionAcceptButton", "Yes"),
                question_text.get("questionCancelButton", "No")
            )
            if question_dialog.exec() == dialog.DialogCode.Accepted:
                helpers = Helpers()
                SettingsManager.reset_application_settings(self.main_window, dialog, helpers)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def show_progress_dialog(self, parent: QWidget) -> None:
        try:
            progress_dialog = ProgressDialog(False, parent)
            dialog_text = LanguageProvider.get_dialog_text(LanguageProvider.usage_language,
                                                           progress_dialog.objectName())
            progress_dialog.setup_dialog(dialog_text.get("labelText", "Loading..."), 0,
                                         dialog_text.get("onFinished", "Completed"))
            progress_dialog.show()
            project_name = self.main_window.project_name_label.text()
            if project_name:
                ProjectsProvider.set_project_path(project_name, ProjectsProvider.project_path)
            self.count_manager.set_files_list(ProjectsProvider.project_path)
            self.count_manager.files_count_thread.finished.connect(progress_dialog.close)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.class_name)

    def set_statistics_data(self, dialog: StatisticsDialog, index: int, total_text: str, code_text: str, empty_text: str,
                            comments_text: str) -> None:
        try:
            project_name = dialog.project_combobox.itemText(index)
            if not self.projects_data:
                raise ValueError("Project data error")
            results = self.projects_data.get(project_name, {}).get("results", {})
            project_data_results = ProjectsManager.get_project_statistics_data(results)
            total_count_data = project_data_results.get("total", {})
            progress_data = project_data_results.get("progressCount", {})
            if not total_count_data or not progress_data or not results:
                dialog.update_values("N/A", "N/A", "N/A", "N/A")
                raise ValueError("Project data error")
            dialog.update_values(total_count_data.get("total", "N/A"), total_count_data.get("code", "N/A"),
                                 total_count_data.get("empty", "N/A"), total_count_data.get("comments", "N/A"))
            dialog.progress_graph_widget.set_plot_data(progress_data.get("x_progress", []), progress_data.get("y_progress", []),
                                                       results, total_text, code_text, empty_text, comments_text)
            if not dialog.count_widget.isVisible():
                dialog.set_visible()
        except Exception as e: ErrorHandler.exception_handler(e, self.class_name)