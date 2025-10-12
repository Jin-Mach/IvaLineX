from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QComboBox

from src.core.providers.projects_provider import ProjectsProvider, BASE_DIR
from src.utilities.error_handler import ErrorHandler
from src.utilities.helpers import Helpers

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow

class ProjectsManager:
    class_name = "projectsManager"

    @staticmethod
    def create_project_file(project_name: str) -> bool:
        try:
            if not project_name:
                raise NameError("Empty project name")
            if not ProjectsProvider.create_file(project_name):
                raise FileExistsError("Project file already exists or cannot be created.")
            return True
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name, show_details=False)
            return False

    @staticmethod
    def set_selected_project(projects_combobox: QComboBox) -> bool:
        try:
            projects_list = ProjectsProvider.get_projects_names()
            validated_names = []
            if not projects_list:
                raise LookupError("No saved projects found")
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
            ProjectsProvider.project_path = project_path
            main_window.project_name_label.setText(project_name)
            metrics = QFontMetrics(main_window.folder_line_input.font())
            short_path = metrics.elidedText(str(project_path), Qt.TextElideMode.ElideLeft, main_window.folder_line_input.width())
            main_window.folder_line_input.setText(short_path)
            main_window.folder_line_input.setToolTip(str(project_path))
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name)