import logging
import os
import sys
from pythonjsonlogger import jsonlogger


def get_logger(service_name: str):
    logger = logging.getLogger(service_name)

    if logger.handlers:
        return logger

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger