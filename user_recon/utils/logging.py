# user_recon/util/logging.py

import logging
import os
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init

# Initialize colorama for cross-platform
init(autoreset=True)


class LogManager:
    """
    Centralized logging utility with color output + rotating file logs.
    """

    LEVEL_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def __init__(self, log_dir="logs", log_file="user_recon.log"):
        os.makedirs(log_dir, exist_ok=True)
        self.log_path = os.path.join(log_dir, log_file)

        # Base logger
        self.logger = logging.getLogger("UserRecon")
        self.logger.setLevel(logging.DEBUG)

        # Console handler (with colors)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.ColorFormatter())

        # Rotating file handler
        file_handler = RotatingFileHandler(
            self.log_path, maxBytes=2 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        # Attach handlers if not already attached
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    class ColorFormatter(logging.Formatter):
        """Custom formatter for colored console logs."""

        def format(self, record):
            color = LogManager.LEVEL_COLORS.get(record.levelno, "")
            reset = Style.RESET_ALL
            return f"{color}{record.levelname:<8}{reset} {record.getMessage()}"

    # -------------------------------
    # Shortcut methods
    # -------------------------------
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)


# Global logger instance
log = LogManager().logger

if __name__ == "__main__":
    lm = LogManager()
    lm.info("System initialized.")
    lm.debug("Debugging mode active.")
    lm.warning("Suspicious activity detected.")
    lm.error("Failed to connect to service.")
    lm.critical("Critical system failure.")
