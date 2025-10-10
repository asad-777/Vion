import os 
from logger import logger
import json
from config import PERSISTENCE_FILE, DEFAULT_COUNTER_VALUE

def load_data():
    if os.path.exists(PERSISTENCE_FILE):
        with open(PERSISTENCE_FILE, 'r') as f:
            try:
                data = json.load(f)
                logger.info(f"{"counter"} loaded from {PERSISTENCE_FILE}: {data}")
                return data.get("counter", DEFAULT_COUNTER_VALUE)
            except json.JSONDecodeError:
                logger.warning("Warning: Corrupted JSON file.")
                return DEFAULT_COUNTER_VALUE
    return DEFAULT_COUNTER_VALUE

def save_data(counter_value):
    data = {"counter": counter_value}
    with open(PERSISTENCE_FILE, 'w') as f:
        json.dump(data, f)