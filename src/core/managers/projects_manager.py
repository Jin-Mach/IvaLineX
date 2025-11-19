import pathlib
import traceback

from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QComboBox

from src.core.providers.language_provider import LanguageProvider
from src.core.providers.projects_provider import ProjectsProvider, BASE_DIR
from src.ui.dialogs.error_dialog import ErrorDialog
from src.utilities.error_handler import ErrorHandler
from src.utilities.helpers import Helpers

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow

class ProjectsManager:
    class_name = "projectsManager"

    @staticmethod
    def create_project_file(main_window: "MainWindow", project_name: str, current_time: str) -> bool:
        try:
            if not project_name:
                raise NameError("Empty project name")
            if not ProjectsProvider.create_file(project_name, current_time):
                error_text = LanguageProvider.get_error_text("FileExistsError")
                dialog = ErrorDialog(error_text, traceback.format_exc(), show_details_button=False, parent=main_window)
                dialog.exec()
                return False
            return True
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name, show_details=False)
            return False

    @staticmethod
    def set_selected_project(main_window: "MainWindow", projects_combobox: QComboBox) -> bool:
        try:
            projects_list = ProjectsProvider.get_projects_names()
            validated_names = []
            if not projects_list:
                error_text = LanguageProvider.get_error_text("LookupError")
                dialog = ErrorDialog(error_text, traceback.format_exc(), show_details_button=False, parent=main_window)
                dialog.exec()
                return False
            for project in projects_list:
                validated_names.append(Helpers.validate_project_name(project, True).removesuffix(".json"))
            projects_combobox.addItems(sorted(validated_names))
            return True
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name, show_details=False)
            return False

    @staticmethod
    def set_application_to_project(main_window: "MainWindow", project_name: str) -> None:
        try:
            validated_project_name = Helpers.validate_project_name(project_name, False)
            project_path = BASE_DIR.joinpath(validated_project_name)
            main_window.project_name_label.setText(project_name)
            project_info = ProjectsProvider.get_project_info(project_path)
            if project_info:
                current_project_path = project_info.get("projectPath", "")
                ProjectsProvider.project_path = current_project_path
                if current_project_path:
                    metrics = QFontMetrics(main_window.folder_line_input.font())
                    short_path = metrics.elidedText(str(current_project_path), Qt.TextElideMode.ElideLeft, main_window.folder_line_input.width())
                    main_window.folder_line_input.setText(short_path)
                    main_window.folder_line_input.setToolTip(current_project_path)
                    ProjectsManager.update_project_path(project_name, current_project_path)
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name)

    @staticmethod
    def close_selected_project(main_window: "MainWindow") -> None:
        try:
            ProjectsManager.close_project_ui(main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name)

    @staticmethod
    def delete_selected_project(main_window: "MainWindow", project_name: str) -> None:
        try:
            project_dir = Helpers.validate_project_name(project_name, False)
            project_path = BASE_DIR.joinpath(project_dir)
            project_path = pathlib.Path(project_path)
            if project_path.is_file() and project_path.suffix == ".json":
                project_path.unlink()
            main_window.project_name_label.setText("")
            ProjectsManager.close_selected_project(main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name)

    @staticmethod
    def update_project_path(projects_name: str, project_path: str) -> None:
        try:
            if projects_name:
                ProjectsProvider.project_path = project_path
                if not ProjectsProvider.set_project_path(projects_name, ProjectsProvider.project_path):
                    raise ValueError("Update project path error")
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name)

    @staticmethod
    def close_project_ui(main_window: "MainWindow") -> None:
        try:
            main_window.folder_line_input.setText("")
            main_window.folder_line_input.setToolTip("")
            main_window.folder_list_view.model.setStringList([])
            main_window.files_count_label.setText("?")
            ProjectsProvider.project_path = ""
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name)

    @staticmethod
    def project_results_handler(main_window: "MainWindow", settings_data: dict[str, dict[str, Any]], results: dict[str, int]) -> None:
        try:
            saved_results ={
                "code": results.get("code", 0),
                "empty": 0,
                "comments": 0
            }
            validate_project_name = Helpers.validate_project_name(main_window.project_name_label.text(), False)
            if not main_window.project_name_label.text() or not main_window.save_history_checkbox.isChecked():
                return
            python_settings = settings_data.get("python_settings")
            if python_settings.get("emptyRowsCheckboxUser", False):
                saved_results["empty"] = results.get("empty", 0)
            if python_settings.get("commentsCheckboxUser", False):
                saved_results["comments"] = results.get("comments", 0)
            ui_text = LanguageProvider.get_text(LanguageProvider.usage_language, "ui_text").get("mainWindow", {})
            result_saved = ui_text.get(f"{main_window.status_bar.objectName()}Saved", "Saved...")
            result_not_saved = ui_text.get(f"{main_window.status_bar.objectName()}NotSaved", "Error while saving...")
            result = ProjectsProvider.project_path and ProjectsProvider.save_project_results(validate_project_name, saved_results)
            if result:
                main_window.status_bar.showMessage(result_saved, 5000)
            else:
                main_window.status_bar.showMessage(result_not_saved, 5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name)

    @staticmethod
    def get_statistics_data() -> dict[str, dict[str, str | dict[str, int]]]:
        try:
            all_projects = {}
            for project in BASE_DIR.iterdir():
                if project.is_file() and project.name.endswith(".json"):
                    project_data = ProjectsProvider.get_project_info(project)
                    project_structure = {
                        "projectPath": project_data.get("projectPath", ""),
                        "created": project_data.get("created", ""),
                        "results": project_data.get("results", {})
                    }
                    all_projects[project.name] = project_structure
            return all_projects
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name)
            return {}