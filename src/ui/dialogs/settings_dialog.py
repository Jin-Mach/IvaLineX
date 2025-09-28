from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QCheckBox, QTabWidget, QDialogButtonBox, QComboBox

from src.ui.dialogs.widgets.python_widget import PythonWidget


# noinspection PyTypeChecker
class SettingsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("settingsDialog")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.RestoreDefaults | QDialogButtonBox.StandardButton.Ok
                                      | QDialogButtonBox.StandardButton.Cancel)
        self.reset_button = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        self.reset_button.setObjectName("resetButton")
        self.save_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.save_button.setObjectName("saveButton")
        self.cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        self.cancel_button.setObjectName("cancelButton")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.create_basic_ui())
        main_layout.addWidget(self.create_language_gui())
        main_layout.addWidget(self.create_common_gui())
        main_layout.addWidget(button_box)
        return main_layout

    def create_basic_ui(self) -> QGroupBox:
        self.basic_groupbox = QGroupBox()
        self.basic_groupbox.setObjectName("basicGroupbox")
        basic_layout = QVBoxLayout()
        language_layout = QHBoxLayout()
        self.language_label_text = QLabel()
        self.language_label_text.setObjectName("languageLabelText")
        self.language_combobox = QComboBox()
        self.language_combobox.setObjectName("languageCombobox")
        folder_layout = QHBoxLayout()
        self.folder_label_text = QLabel()
        self.folder_label_text.setObjectName("folderLabelText")
        self.folder_edit = QLineEdit()
        self.folder_edit.setObjectName("folderEdit")
        self.folder_edit.setReadOnly(True)
        self.select_folder_button = QPushButton()
        self.select_folder_button.setObjectName("selectFolderButton")
        history_layout = QHBoxLayout()
        self.history_checkbox = QCheckBox()
        self.history_checkbox.setObjectName("historyCheckbox")
        language_layout.addWidget(self.language_label_text)
        language_layout.addWidget(self.language_combobox)
        language_layout.addStretch()
        folder_layout.addWidget(self.folder_label_text)
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(self.select_folder_button)
        history_layout.addWidget(self.history_checkbox)
        history_layout.addStretch()
        basic_layout.addLayout(language_layout)
        basic_layout.addLayout(folder_layout)
        basic_layout.addLayout(history_layout)
        self.basic_groupbox.setLayout(basic_layout)
        return self.basic_groupbox

    def create_language_gui(self) -> QGroupBox:
        self.language_groupbox = QGroupBox()
        self.language_groupbox.setObjectName("languageGroupbox")
        language_layout = QVBoxLayout()
        self.language_tab = QTabWidget()
        self.language_tab.setObjectName("languageTab")
        language_layout.addWidget(self.language_tab)
        self.python_tab = PythonWidget(self)
        self.language_tab.addTab(self.python_tab, "Python")
        self.language_groupbox.setLayout(language_layout)
        return self.language_groupbox

    def create_common_gui(self) -> QGroupBox:
        self.common_groupbox = QGroupBox()
        self.common_groupbox.setObjectName("commonGroupbox")
        common_layout = QVBoxLayout()
        self.json_checkbox = QCheckBox()
        self.json_checkbox.setObjectName("jsonCheckbox")
        self.readme_checkbox = QCheckBox()
        self.readme_checkbox.setObjectName("readmeCheckbox")
        self.ignore_files_checkbox = QCheckBox()
        self.ignore_files_checkbox.setObjectName("ignoreFilesCheckbox")
        self.ignore_binary_checkbox = QCheckBox()
        self.ignore_binary_checkbox.setObjectName("ignoreBinaryCheckbox")
        common_layout.addWidget(self.json_checkbox)
        common_layout.addWidget(self.readme_checkbox)
        common_layout.addWidget(self.ignore_files_checkbox)
        common_layout.addWidget(self.ignore_binary_checkbox)
        self.common_groupbox.setLayout(common_layout)
        return self.common_groupbox

    def set_ui_text(self, title: str, reset: str, save: str, cancel: str) -> None:
        self.setWindowTitle(title)
        self.reset_button.setText(reset)
        self.save_button.setText(save)
        self.cancel_button.setText(cancel)

    def set_basic_ui_text(self, title: str, language: str, folder: str, edit: str, button: str, history: str) -> None:
        self.basic_groupbox.setTitle(title)
        self.language_label_text.setText(language)
        self.folder_label_text.setText(folder)
        if not self.folder_edit.text():
            self.folder_edit.setPlaceholderText(edit)
        self.select_folder_button.setText(button)
        self.history_checkbox.setText(history)

    def set_language_ui_text(self, title: str) -> None:
        self.language_groupbox.setTitle(title)

    def set_common_ui_text(self, title: str, json: str, readme: str, files: str, binary: str) -> None:
        self.common_groupbox.setTitle(title)
        self.json_checkbox.setText(json)
        self.readme_checkbox.setText(readme)
        self.ignore_files_checkbox.setText(files)
        self.ignore_binary_checkbox.setText(binary)

    def showEvent(self, event) -> None:
        self.setFixedSize(500, self.height())
        super().showEvent(event)