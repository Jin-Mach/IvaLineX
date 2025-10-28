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
    ],
    "init": [],
    "setup": [
        fake_project.joinpath("setup.py")
    ],
    "main": [fake_project.joinpath("__main__.py")],
    "venv": [],
    "tests": [
        test_folder.joinpath("fake_test.py")],
    "config": [
        config_folder.joinpath("fake_toml.toml"),
        cs_folder.joinpath("cs_fake_one.json")
    ],
    "documentation": [
        fake_project.joinpath("readme.md"),
        fake_project.joinpath("requirements.txt"),
        fake_project.joinpath("license")
    ],
    "binary": [fake_project.joinpath("fake_binary.bin")],
    "large": []
}

count_list = [
    #fake_app: 3, 1, 1
    fake_project.joinpath("fake_run_app.py"),
    #fake main: 1, 1, 3
    src_folder.joinpath("fake_main.py"),
    #fake main window: 1, 1, 1
    ui_folder.joinpath("fake_main_window.py"),
    #fake __main__: 1, 0, 0
    fake_project.joinpath("__main__.py"),
    #fake setup: 7, 2, 1
    fake_project.joinpath("setup.py"),
    #fake test: 1, 0, 0
    test_folder.joinpath("fake_test.py"),
    #fake toml: 7, 3, 0
    config_folder.joinpath("fake_toml.toml"),
    #fake json: 7, 1, 0
    cs_folder.joinpath("cs_fake_one.json"),
    #fake readme: 6, 5, 0
    fake_project.joinpath("readme.md"),
    #fake requirements: 3, 1, 0
    fake_project.joinpath("requirements.txt"),
    #fake license: 5, 2, 0
    fake_project.joinpath("license"),
    #fake binary: 4, 0, 0
    fake_project.joinpath("fake_binary.bin")
    #total: 46, 17, 6
]

def test_get_items_types() -> None:
    result = CountProvider.get_items_types(str(fake_project))
    correct_sorted = {}
    for key, value in correct_result.items():
        sorted_value = sorted(value)
        correct_sorted[key] = sorted_value
        try:
            assert result[key] == correct_sorted[key]
        except AssertionError:
            error_msg = get_items_error_text(key, result[key], correct_sorted[key])
            pytest.fail(error_msg)

def get_items_error_text(key: str, result_list: list[Path], sorted_list: list[Path]) -> str:
    set_result = set(result_list) - set(sorted_list)
    set_sorted = set(sorted_list) - set(result_list)
    missing_text = ""
    if set_result:
        missing_text = f"\nresult miss: {set_result}"
    if set_sorted:
        missing_text += f"\ncorrect_sorted miss: {set_sorted}"
    return f"Assert error: result key: '{key}'\nmissing item(s): {len(set_result) + len(set_sorted)}{missing_text}"

def test_count_project_rows() -> None:
    correct = {"code": 46, "empty": 17, "comments": 6}
    result = CountProvider.count_project_rows(count_list)
    assert result == correct