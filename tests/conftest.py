import os
import tempfile

from src.utils.logging_config import setup_logging

# Configure logging for all test sessions to print to console
setup_logging(log_file=os.path.join(tempfile.gettempdir(), "test_run.log"))
