import logging
import sys
from datetime import datetime
from pathlib import Path

from .config import LOG_BASE_DIR, LOG_FORMAT


class DateBasedFileHandler(logging.Handler):
    """Write logs into date-based folders: log/YYYY-MM-DD/server.log."""

    def __init__(self, base_log_dir: Path, filename: str = "server.log", encoding: str = "utf-8"):
        super().__init__()
        self.base_log_dir = base_log_dir
        self.filename = filename
        self.encoding = encoding
        self.current_date = None
        self.file_handler = None
        self._refresh_handler_if_needed()

    def _refresh_handler_if_needed(self):
        date_str = datetime.now().strftime("%Y-%m-%d")
        if self.current_date == date_str and self.file_handler:
            return

        if self.file_handler:
            self.file_handler.close()

        day_dir = self.base_log_dir / date_str
        day_dir.mkdir(parents=True, exist_ok=True)
        file_path = day_dir / self.filename

        self.file_handler = logging.FileHandler(file_path, encoding=self.encoding)
        if self.formatter:
            self.file_handler.setFormatter(self.formatter)
        self.current_date = date_str

    def emit(self, record):
        try:
            self._refresh_handler_if_needed()
            self.file_handler.emit(record)
        except Exception:
            self.handleError(record)

    def setFormatter(self, fmt):
        super().setFormatter(fmt)
        if self.file_handler:
            self.file_handler.setFormatter(fmt)

    def close(self):
        if self.file_handler:
            self.file_handler.close()
        super().close()


def configure_logging() -> logging.Logger:
    """Configure root logger with console and date-based file handlers."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers = []

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    date_file_handler = DateBasedFileHandler(LOG_BASE_DIR)
    date_file_handler.setLevel(logging.DEBUG)
    date_file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(date_file_handler)

    return logging.getLogger(__name__)
