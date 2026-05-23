import logging
from logging.handlers import TimedRotatingFileHandler

from pathlib import Path
from datetime import datetime

from shared.config import load_yaml_config
from shared.paths import CONFIG_DIR

# Load config
CONFIG_PATH = CONFIG_DIR / "training.yaml"
config = load_yaml_config(CONFIG_PATH)

# Logging level
LOG_LEVEL = getattr(logging, config.get("logging", {}).get("level", "INFO"))

# Logs directory
LOG_DIR = Path(config.get("logging", {}).get("log_dir", "logs"))

LOG_DIR.mkdir(parents=True, exist_ok=True)


# Daily log file
LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y')}.log"
LOG_FILE_PATH = LOG_DIR / LOG_FILE


# Create module logger
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


# Prevent duplicate handlers
if not logger.handlers:

    # Formatter
    formatter = logging.Formatter(
        "[ %(asctime)s ] %(filename)s:%(lineno)d "
        "%(funcName)s - %(levelname)s - %(message)s"
    )

    # Rotating file handler
    file_handler = TimedRotatingFileHandler(
        filename=LOG_FILE_PATH, when="midnight", interval=1, backupCount=7
    )

    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
