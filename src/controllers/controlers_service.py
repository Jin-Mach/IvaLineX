from typing import TYPE_CHECKING

from src.controllers.dialogs_controler import DialogsController
from src.controllers.main_controler import MainController
from src.core.managers.count_manager import CountManager

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow
    from src.ui.widgets.menu_bar import MenuBar


class ControllersService:
    def __init__(self, main_window: "MainWindow", menu_bar: "MenuBar") -> None:
        self.count_manager = CountManager(main_window)
        self.dialog_controller = DialogsController(main_window, menu_bar, self.count_manager)
        self.main_controller = MainController(main_window, self.count_manager)
