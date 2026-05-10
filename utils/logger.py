import logging
import sys
from pathlib import Path

# Ensure logs/ directory exists before anything else runs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"


def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger that writes INFO+ to stdout
    and DEBUG+ to logs/app.log.

    Calling this multiple times with the same name is safe —
    handlers are only attached once.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # already configured

    logger.setLevel(logging.DEBUG)

    # --- Console: INFO and above ---
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))

    # --- File: everything DEBUG and above ---
    file_h = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_h.setLevel(logging.DEBUG)
    file_h.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    ))

    logger.addHandler(console)
    logger.addHandler(file_h)
    logger.propagate = False

    return logger