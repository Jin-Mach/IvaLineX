from typing import TYPE_CHECKING, Any

import pathlib
import tomllib

from PyQt6.QtWidgets import QWidget

from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.ui.dialogs.settings_dialog import SettingsDialog

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.joinpath("config", "app_settings.toml")


# noinspection PyUnresolvedReferences
class SettingsProvider:
    class_name = "settingsProvider"

    @staticmethod
    def apply_settings_dialog_config(dialog: "SettingsDialog") -> None:
        try:
            toml_data = SettingsProvider.get_toml_data()
            for widget in dialog.findChildren(QWidget):
                for section in ["language_settings", "path_settings", "history_settings", "python_settings"]:
                    value = toml_data.get(section, {}).get(f"{widget.objectName()}User", {})
                    if value:
                        if hasattr(widget, "addItems"):
                            widget.clear()
                            if isinstance(value, list):
                                widget.addItems(value)
                        if hasattr(widget, "setText"):
                            widget.setText(str(value))
                        if hasattr(widget, "setChecked"):
                            widget.setChecked(bool(value))
        except Exception as e:
            ErrorHandler.exception_handler(e, SettingsProvider.class_name)

    @staticmethod
    def get_toml_data() -> dict[str, Any]:
        try:
            if not BASE_DIR.exists() or BASE_DIR.stat().st_size == 0:
                raise FileNotFoundError(f"Toml file not found: {BASE_DIR}")
            with open(BASE_DIR, "rb") as toml_file:
                toml_data = tomllib.load(toml_file)
                return toml_data
        except Exception as e:
            ErrorHandler.exception_handler(e, SettingsProvider.class_name)
            return {}