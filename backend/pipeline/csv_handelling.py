from config import CSV_FILE_PATH,UPDATE_COUNTER
from typing import Optional
from logger import logger
import pandas as pd #type:ignore
from system_variable import load_data, save_data

df = None
link_count = load_data()
len_df = 0

# read entire csv file
def csv_read(path=CSV_FILE_PATH):
    global df
    global len_df
    try:
        df = pd.read_csv(path)
        logger.info(f"CSV file read successfully from {path}")
        if len_df == 0:
            len_df = len(df)
        return df
    except FileNotFoundError:
        logger.error(f"Error: CSV file not found at path: {path}")
        # Return an empty DataFrame or None to signal failure
        return None
    except pd.errors.EmptyDataError:
        logger.warning(f"Warning: No columns to parse from file at path: {path}. File might be empty.")
        return None
    except pd.errors.ParserError:
        logger.error(f"Error: Malformed CSV format in file at path: {path}. Check delimiters or structure.")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while reading the CSV file: {e}")
        return None

 
def return_link() -> Optional[str]:
    global df
    global link_count
    global len_df
    if df is None:
        df = csv_read()
    if df is not None and not df.empty:
        
        if link_count < len_df:
            title = str(df.iloc[link_count,0]).strip()
            link = str(df.iloc[link_count,1]).strip()
            logger.info(f"Link returned: {link_count} with title {title}")
            if UPDATE_COUNTER:
                link_count += 1
                save_data(link_count)
            return link
        else:
            logger.warning("Link count exceeds number of links in CSV.")
            return None
    else:
        logger.error("DataFrame is empty or None.")
        return None