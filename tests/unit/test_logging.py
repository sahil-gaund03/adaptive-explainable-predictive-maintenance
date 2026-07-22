import json
import logging
import os
import tempfile
from collections.abc import Generator

import pytest
from src.utils.logging_config import setup_logging


@pytest.fixture
def temp_log_file() -> Generator[str, None, None]:
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        temp_path = f.name
    yield temp_path

    # Close logging handlers to release file lock on Windows
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        handler.close()
        root_logger.removeHandler(handler)

    if os.path.exists(temp_path):
        os.remove(temp_path)


def test_json_logging(temp_log_file: str) -> None:
    # Setup logging to temporary file
    setup_logging(default_level=logging.INFO, log_file=temp_log_file)

    logger = logging.getLogger("test_json_logging_logger")

    # Log messages
    logger.info(
        "Test message info", extra={"sample_index": 42, "model_type": "xgboost"}
    )
    logger.debug(
        "Test message debug"
    )  # Should be logged to file since file handler is DEBUG

    # Read log file and verify JSON format
    with open(temp_log_file, encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) >= 2

    # Parse and assert first log line (INFO)
    info_log = json.loads(lines[0])
    assert info_log["level"] == "INFO"
    assert info_log["name"] == "test_json_logging_logger"
    assert info_log["message"] == "Test message info"
    assert info_log["sample_index"] == 42
    assert info_log["model_type"] == "xgboost"
    assert "timestamp" in info_log

    # Parse and assert second log line (DEBUG)
    debug_log = json.loads(lines[1])
    assert debug_log["level"] == "DEBUG"
    assert debug_log["message"] == "Test message debug"
