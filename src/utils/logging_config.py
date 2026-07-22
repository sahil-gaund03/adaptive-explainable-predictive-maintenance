import json
import logging
import logging.handlers
import os
from datetime import datetime
from typing import Any


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: dict[str, Any] = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }

        # Include custom exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Include any extra attributes passed to the logger
        # Ignore standard LogRecord attributes
        standard_attrs = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
        }

        for key, value in record.__dict__.items():
            if key not in standard_attrs and not key.startswith("_"):
                log_data[key] = value

        return json.dumps(log_data)


def setup_logging(
    default_level: int = logging.INFO, log_file: str = "experiment.log"
) -> None:
    """Sets up python standard logging with a JSON formatter for console and file."""
    # Ensure log directory exists if file path contains a directory
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    root_logger = logging.getLogger()
    # Set to DEBUG so all messages flow to the handlers
    root_logger.setLevel(logging.DEBUG)

    # Clear existing handlers
    root_logger.handlers = []

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    console_handler.setLevel(default_level)
    root_logger.addHandler(console_handler)

    # File Handler (Rotating log file, max 10MB, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(JSONFormatter())
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
