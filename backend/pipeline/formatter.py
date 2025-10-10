from logger import logger
from scrapper import scrape_website
from typing import Optional

def format_data() -> Optional[str]:
    data = scrape_website()
    return data