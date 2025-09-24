from src.utilities.logger_provider import get_logger


class ErrorHandler:
    logger = get_logger()

    @staticmethod
    def exception_handler(exception: Exception, class_name: str = "Global") -> None:
        ErrorHandler.logger.error(f"{class_name}: {exception}", exc_info=True)