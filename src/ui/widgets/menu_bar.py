from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu


class MenuBar(QMenuBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("menuBar")
        self.create_gui()

    def create_gui(self) -> None:
        project_menu = QMenu(self)
        project_menu.setObjectName("projectMenu")
        new_project_action = QAction(self)
        new_project_action.setObjectName("newProjectAction")
        open_project_action = QAction(self)
        open_project_action.setObjectName("openProjectAction")
        close_project_action = QAction(self)
        close_project_action.setObjectName("closeProjectAction")
        settings_action = QAction(self)
        settings_action.setObjectName("settingsAction")
        close_app_action = QAction(self)
        close_app_action.setObjectName("closeAppAction")
        project_menu.addAction(new_project_action)
        project_menu.addAction(open_project_action)
        project_menu.addAction(close_project_action)
        project_menu.addSeparator()
        project_menu.addAction(settings_action)
        project_menu.addSeparator()
        project_menu.addAction(close_app_action)
        info_menu = QMenu(self)
        info_menu.setObjectName("infoMenu")
        manual_action = QAction(self)
        manual_action.setObjectName("manualAction")
        about_action = QAction(self)
        about_action.setObjectName("aboutAction")
        info_menu.addAction(manual_action)
        info_menu.addAction(about_action)
        self.addMenu(project_menu)
        self.addMenu(info_menu)