import logging

from pathlib import Path
from datetime import datetime

from src.config import load_yaml_config
from src.paths import CONFIG_DIR

# Load config
CONFIG_PATH = CONFIG_DIR / "training.yaml"

config = load_yaml_config(CONFIG_PATH)

# Logging level
LOG_LEVEL = getattr(
    logging,
    config["logging"]["level"]
)

# Logs directory
LOG_DIR = Path(config["logging"]["log_dir"])

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Daily log file
LOG_FILE = ( f"{datetime.now().strftime('%d_%m_%Y')}.log")
LOG_FILE_PATH = LOG_DIR / LOG_FILE

# Create module logger
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Prevent duplicate handlers
if not logger.handlers:

    # Common log formatter
    formatter = logging.Formatter(
        "[ %(asctime)s ] %(lineno)d %(name)s - "
        "%(levelname)s - %(message)s"
    )

    # File handler
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)