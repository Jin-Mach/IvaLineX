import logging
import pathlib

from logging.handlers import RotatingFileHandler

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

def get_logger() -> logging.Logger:
    log_path = BASE_DIR.joinpath("logs")
    log_path.mkdir(parents=True, exist_ok=True)
    logger  = logging.getLogger("IvalineXLogger")
    logger.setLevel(logging.WARNING)
    handler = RotatingFileHandler(log_path.joinpath("ivaLines.log"), maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s - %(funcName)s - %(lineno)d",
                                  datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(handler)
    return logger