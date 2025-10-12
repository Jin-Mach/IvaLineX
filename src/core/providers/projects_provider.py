import pathlib

from src.utilities.error_handler import ErrorHandler
from src.utilities.helpers import Helpers

BASE_DIR = pathlib.Path(__file__).parents[3].joinpath("projects")
BASE_DIR.mkdir(parents=True, exist_ok=True)


class ProjectsProvider:
    class_name = "projectsProvider"
    project_path = None

    @staticmethod
    def create_file(project_name: str) -> bool:
        try:
            file_name = Helpers.validate_project_name(project_name, False)
            if BASE_DIR.exists() and file_name not in ProjectsProvider.get_projects_names():
                BASE_DIR.joinpath(file_name).touch()
                ProjectsProvider.project_path = BASE_DIR.joinpath(file_name)
                return True
            return False
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsProvider.class_name, show_details=False)
            return False

    @staticmethod
    def get_projects_names() -> list[str]:
        try:
            projects = []
            for file in BASE_DIR.glob("*.json"):
                projects.append(file.name)
            return projects
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsProvider.class_name, show_details=False)
            return []