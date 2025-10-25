from pathlib import Path

import pytest

from src.core.providers.count_provider import CountProvider

fake_project = Path(__file__).parent.joinpath("fake_project")
src_folder = fake_project.joinpath("fake_src")
ui_folder = src_folder.joinpath("fake_ui")
widgets_folder = ui_folder.joinpath("fake_widgets")
utilities_folder = src_folder.joinpath("fake_utilities")
test_folder = fake_project.joinpath("test")
lib_folder = fake_project.joinpath("venv").joinpath("fake_lib")
config_folder = fake_project.joinpath("fake_config")
language_folder = fake_project.joinpath("fake_languages")
cs_folder = language_folder.joinpath("fake_cs")
en_folder = language_folder.joinpath("fake_en")

correct_result = {
    "code": [
        fake_project.joinpath("fake_run_app.py"),
        src_folder.joinpath("fake_main.py"),
        ui_folder.joinpath("fake_main_window.py"),
        ui_folder.joinpath("fake_second_window.py"),
        widgets_folder.joinpath("fake_widget_one.py"),
        utilities_folder.joinpath("fake_utility_first.py"),
        utilities_folder.joinpath("fake_utility_second.py"),
        utilities_folder.joinpath("fake_utility_third.py")
    ],
    "init": [
        src_folder.joinpath("__init__.py"),
        ui_folder.joinpath("__init__.py"),
        widgets_folder.joinpath("__init__.py"),
        utilities_folder.joinpath("__init__.py")
    ],
    "setup": [
        fake_project.joinpath("setup.py")
    ],
    "main": [fake_project.joinpath("__main__.py")],
    "venv": [lib_folder.joinpath("fake_pytest")],
    "tests": [
        test_folder.joinpath("__init__.py"),
        test_folder.joinpath("fake_test.py")],
    "config": [
        config_folder.joinpath("fake_toml.toml"),
        cs_folder.joinpath("cs_fake_one.json"),
        cs_folder.joinpath("cs_fake_second.json"),
        en_folder.joinpath("en_fake_one.json"),
        en_folder.joinpath("en_fake_second.json"),
        language_folder.joinpath("fake_map.json")
    ],
    "documentation": [
        fake_project.joinpath("readme.md"),
        fake_project.joinpath("requirements.txt"),
        fake_project.joinpath("license")
    ],
    "binary": [fake_project.joinpath("fake_binary.bin")],
    "large": []
}

def test_get_items_types() -> None:
    result = CountProvider.get_items_types(str(fake_project))
    correct_sorted = {}
    for key, value in correct_result.items():
        sorted_value = sorted(value)
        correct_sorted[key] = sorted_value
        try:
            assert result[key] == correct_sorted[key]
        except AssertionError:
            error_msg = get_error_text(key, result[key], correct_sorted[key])
            pytest.fail(error_msg)

def get_error_text(key: str, result_list: list[Path], sorted_list: list[Path]) -> str:
    set_result = set(result_list) - set(sorted_list)
    set_sorted = set(sorted_list) - set(result_list)
    missing_text = ""
    if set_result:
        missing_text = f"\nresult miss: {set_result}"
    if set_sorted:
        missing_text += f"\ncorrect_sorted miss: {set_sorted}"
    return f"Assert error: result key: '{key}'\nmissing item(s): {len(set_result) + len(set_sorted)}{missing_text}"