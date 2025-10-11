from logger import logger
from scrapper import final_data
from typing import Optional
from bs4 import BeautifulSoup  # type: ignore

def format_data() :
    
    
    data = final_data()
    if data is None:
        return "None data"
    
    return data