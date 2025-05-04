import logging
from logging_loki import LokiHandler

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    # Консольный вывод
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    ))
    logger.addHandler(console_handler)

    # Loki Handler
    loki_handler = LokiHandler(
        url="http://localhost:3100/loki/api/v1/push",  # URL Loki
        tags={"application": "fastapi-app"},
        version="1",
    )
    loki_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    ))
    logger.addHandler(loki_handler)

    return logger
