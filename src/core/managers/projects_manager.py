from src.core.providers.projects_provider import ProjectsProvider
from src.utilities.error_handler import ErrorHandler


class ProjectsManager:
    class_name = "projectsManager"

    @staticmethod
    def create_project_file(project_name: str) -> bool:
        try:
            if not project_name:
                raise NameError("Empty project name.")
            if not ProjectsProvider.create_file(project_name):
                raise FileExistsError("Project file already exists or cannot be created.")
            return True
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsManager.class_name, show_details=False)
            return False