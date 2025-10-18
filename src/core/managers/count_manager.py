from src.core.providers.count_provider import CountProvider
from src.utilities.error_handler import ErrorHandler


class CountManager:
    class_name = "countManager"

    @staticmethod
    def get_total_count(folder_path: str):
        try:
            xxx = CountProvider.get_items_types(folder_path)
            print(xxx)
        except Exception as e:
            ErrorHandler.exception_handler(e, CountManager.class_name)