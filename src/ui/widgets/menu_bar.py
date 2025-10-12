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
        self.new_project_action = QAction(self)
        self.new_project_action.setObjectName("newProjectAction")
        self.open_project_action = QAction(self)
        self.open_project_action.setObjectName("openProjectAction")
        self.close_project_action = QAction(self)
        self.close_project_action.setObjectName("closeProjectAction")
        self.delete_project_action = QAction(self)
        self.delete_project_action.setObjectName("deleteProjectAction")
        self.settings_action = QAction(self)
        self.settings_action.setObjectName("settingsAction")
        self.close_app_action = QAction(self)
        self.close_app_action.setObjectName("closeAppAction")
        project_menu.addAction(self.new_project_action)
        project_menu.addAction(self.open_project_action)
        project_menu.addAction(self.close_project_action)
        project_menu.addAction(self.delete_project_action)
        project_menu.addSeparator()
        project_menu.addAction(self.settings_action)
        project_menu.addSeparator()
        project_menu.addAction(self.close_app_action)
        info_menu = QMenu(self)
        info_menu.setObjectName("infoMenu")
        self.manual_action = QAction(self)
        self.manual_action.setObjectName("manualAction")
        self.about_action = QAction(self)
        self.about_action.setObjectName("aboutAction")
        info_menu.addAction(self.manual_action)
        info_menu.addAction(self.about_action)
        self.addMenu(project_menu)
        self.addMenu(info_menu)