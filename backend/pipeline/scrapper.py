import json
import requests  # type: ignore
from logger import logger
from csv_handelling import return_link
from bs4 import BeautifulSoup  # type: ignore
from bs4.element import Comment  # type: ignore
import re


def scrape_website() :
    url = return_link()
    if not url:
        logger.warning("No valid URL returned by return_link().")
        return None
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup([
            'script', 'style', 'noscript', 'iframe', 'link', 'img', 'picture', 'meta',
            'button', 'svg', 'form', 'header', 'footer', 'head', 'a','table','h4',
            'figure','h5','h6'
        ]):
            tag.decompose()
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
        for _ in range(2):
            for tag in soup.find_all(['div', 'section', 'span']):
                if len(tag.contents) == 1 and getattr(tag.contents[0], 'name', None) in [
                    'div', 'section', 'span', 'p', 'ul', 'ol', 'li'
                ]:
                    tag.unwrap()
                elif not tag.get_text(strip=True):
                    tag.decompose()
        for tag in soup.find_all(True):
            tag.attrs = {}
            if not tag.get_text(strip=True):
                tag.decompose()
        logger.info("HTML of returned data has been cleaned")
        sections = {}
        banned_words = ['permalink', 'resources', 'cite', 'collections', 'actions']
        index = 1


        for tag in soup.find_all(['section']):
                #text = tag.get_text(separator=' ', strip=True)
                text = str(tag)
                if not text:
                    continue
                lower = text.lower()
                if any(bad in lower for bad in banned_words):
                    continue
                if len(text.split()) < 50:
                    continue
                sections[str(index)] = text
                index += 1


        logger.info("json of returned data has been cleaned")



        def trim_json_from_abstract(data: dict) -> dict:
            start_index = None
            for key, value in sorted(data.items(), key=lambda x: int(x[0])):
                if isinstance(value, str):
                    soup = BeautifulSoup(value, 'html.parser')
                    text = soup.get_text(separator=' ', strip=True)
                    if text.startswith("Abstract"):
                        start_index = int(key)
                        break
            if start_index is None:
                return {}
            trimmed_items = [
                (str(i + 1), data[str(j)]) 
                for i, j in enumerate(range(start_index, len(data) + 1)) 
                if str(j) in data
            ]
            return dict(trimmed_items)
        sections = trim_json_from_abstract(sections)
        logger.info("found abstract and structured the json")
        #json_output = json.dumps(sections, ensure_ascii=False, indent=2)
        logger.info("Json returned")
        

        if isinstance(sections, dict) and sections:
            return_text = []

            for key, text in sections.items():
                if re.match(r"^<section\s*>\s*<(h3|p)>", text, re.IGNORECASE):
                    continue
                return_text.append(text)

            answer = "\n\n\n===============================================\n\n\n".join(return_text)
            logger.info("Clean HTML returned")
            return answer

        else:
            return ("empty sections in processing")
    except requests.exceptions.RequestException as e:
        logger.warning(f"Error scraping {url}: {e}")
        return None
