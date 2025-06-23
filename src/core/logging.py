# src/core/logging_config.py

import logging
from logging.handlers import RotatingFileHandler
import os
import sys


def setup_logging():
    """Configura el sistema de logging para toda la aplicación."""

    LOG_DIR = "logs"
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        f"{LOG_DIR}/app.log",
        maxBytes=5 * 1024 * 1024,  
        backupCount=2,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Opcional: Silenciar un poco los logs de uvicorn.access para que no sean tan ruidosos
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
