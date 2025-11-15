import json
import pathlib

from typing import Any

from PyQt6.QtCore import QDateTime

from src.utilities.error_handler import ErrorHandler
from src.utilities.helpers import Helpers

BASE_DIR = pathlib.Path(__file__).parents[3].joinpath("projects")
BASE_DIR.mkdir(parents=True, exist_ok=True)


class ProjectsProvider:
    class_name = "projectsProvider"
    project_path = None

    @staticmethod
    def create_file(project_name: str, current_time: str) -> bool:
        try:
            project_structure = {
                "projectName": project_name,
                "projectPath": "",
                "created": current_time,
                "results": {}
            }
            file_name = Helpers.validate_project_name(project_name, False)
            if BASE_DIR.exists() and file_name not in ProjectsProvider.get_projects_names():
                BASE_DIR.joinpath(file_name).touch()
                ProjectsProvider.project_path = BASE_DIR.joinpath(file_name)
                with open(ProjectsProvider.project_path, "w", encoding="utf-8") as new_data:
                    json.dump(project_structure, new_data, indent=4, ensure_ascii=False)
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

    @staticmethod
    def get_project_info(project_path: pathlib.Path) -> dict[str, Any]:
        try:
            project_info = {
                "projectName": "",
                "projectPath": "",
                "created": "",
                "results": {}
            }
            with open(project_path, "r", encoding="utf-8") as project_file:
                project_data = json.load(project_file)
                project_info["projectName"] = project_data.get("projectName", "")
                project_info["projectPath"] = project_data.get("projectPath", "")
                project_info["created"] = project_data.get("created", "")
                project_info["results"] = project_data.get("results", {})
            return project_info
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsProvider.class_name, show_details=False)
            return {}

    @staticmethod
    def set_project_path(project_name: str, project_path: str) -> bool:
        try:
            file_name = Helpers.validate_project_name(project_name, False)
            if not BASE_DIR.exists() or not file_name:
                return False
            with open(BASE_DIR.joinpath(file_name), "r", encoding="utf-8") as project:
                project_data = json.load(project)
                project_data["projectPath"] = str(project_path)
            with open(BASE_DIR.joinpath(file_name), "w", encoding="utf-8") as new_data:
                json.dump(project_data, new_data, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsProvider.class_name, show_details=False)
            return False

    @staticmethod
    def save_project_results(project_name: str, results: dict[str, int]) -> bool:
        try:
            project_path = pathlib.Path(__file__).parents[3].joinpath("projects").joinpath(project_name)
            if not project_path.exists():
                return False
            with open(project_path, "r", encoding="utf-8") as project_file:
                project_data = json.load(project_file)
                current_time = QDateTime().currentDateTime().toString("yyyy-MM-ddTHH:mm:ss.zzz")
                values_dict = {"code": results.get("code", 0),
                               "empty": results.get("empty", 0),
                               "comments": results.get("comments", 0)}
                project_data.setdefault("results", {})[current_time] = values_dict
            with open(project_path, "w", encoding="utf_8") as new_project_file:
                json.dump(project_data, new_project_file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            ErrorHandler.exception_handler(e, ProjectsProvider.class_name, show_details=False)
            return False