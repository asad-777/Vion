# logger.py
LOG_FILE_PATH = "logs/vion_pipeline.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(filename)s:%(lineno)d - %(levelname)s - %(message)s - %(asctime)s'
LOGGER_NAME = "vion_pipeline"
FILE_LOGGING_ENABLED = False
CONSOLE_LOGGING_ENABLED = False


# csv_handelling.py
CSV_FILE_PATH = "data/links.csv"

# system_variable.py
PERSISTENCE_FILE = "data/persistence.json"
DEFAULT_COUNTER_VALUE = 0