import logging
import os 
from datetime import datetime

# Create log folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(log_dir, exist_ok=True)

# Create log file with timestamp pr day
LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y')}.log"
LOG_FILE_Path = os.path.join(log_dir,LOG_FILE)

# Create logger
logger = logging.getLogger(__name__) # Root logger
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers

if not logger.handlers:


    # File handler
    file_handler = logging.FileHandler(LOG_FILE_Path)
    file_handler.setFormatter(logging.DEBUG)
    file_formatter = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console logging
    console_handler = logging.StreamHandler() # Logs to terminal
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)