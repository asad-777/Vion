import logging
import os
from config import LOG_FILE_PATH, LOG_LEVEL, LOG_FORMAT,LOGGER_NAME,FILE_LOGGING_ENABLED,CONSOLE_LOGGING_ENABLED

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(level)  
file_handler = logging.FileHandler(LOG_FILE_PATH, mode='a')
file_handler.setLevel(level)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
if FILE_LOGGING_ENABLED: # Set to True to enable file logging
    logger.addHandler(file_handler)

if CONSOLE_LOGGING_ENABLED:  # Set to True to enable console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(console_handler)
