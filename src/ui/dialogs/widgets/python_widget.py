from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QCheckBox

from src.utilities.error_handler import ErrorHandler


class PythonWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("pythonWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.init_checkbox = QCheckBox()
        self.init_checkbox.setObjectName("initCheckbox")
        self.setup_checkbox = QCheckBox()
        self.setup_checkbox.setObjectName("setupCheckbox")
        self.main_checkbox = QCheckBox()
        self.main_checkbox.setObjectName("mainCheckbox")
        self.empty_rows_checkbox = QCheckBox()
        self.empty_rows_checkbox.setObjectName("emptyRowsCheckbox")
        self.comments_checkbox = QCheckBox()
        self.comments_checkbox.setObjectName("commentsCheckbox")
        self.ignore_venv_checkbox = QCheckBox()
        self.ignore_venv_checkbox.setObjectName("ignoreVenvCheckbox")
        self.ignore_tests_checkbox = QCheckBox()
        self.ignore_tests_checkbox.setObjectName("ignoreTestsCheckbox")
        main_layout.addWidget(self.init_checkbox)
        main_layout.addWidget(self.setup_checkbox)
        main_layout.addWidget(self.main_checkbox)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.empty_rows_checkbox)
        main_layout.addWidget(self.comments_checkbox)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.ignore_venv_checkbox)
        main_layout.addWidget(self.ignore_tests_checkbox)
        return main_layout

    def set_ui_text(self, init: str, setup: str, main: str, empty: str, comments: str, venv: str, tests: str) -> None:
        self.init_checkbox.setText(init)
        self.setup_checkbox.setText(setup)
        self.main_checkbox.setText(main)
        self.empty_rows_checkbox.setText(empty)
        self.comments_checkbox.setText(comments)
        self.ignore_venv_checkbox.setText(venv)
        self.ignore_tests_checkbox.setText(tests)

    def get_settings_data(self) -> dict[str, bool]:
        try:
            checkbox_list = [self.init_checkbox, self.setup_checkbox, self.main_checkbox, self.empty_rows_checkbox,
                             self.comments_checkbox, self.ignore_venv_checkbox, self.ignore_tests_checkbox]
            settings_data = {}
            for check_box in checkbox_list:
                settings_data.update({f"{check_box.objectName()}User": check_box.isChecked()})
            return settings_data
        except Exception as e:
            ErrorHandler.exception_handler(e, self.objectName())
            return {}