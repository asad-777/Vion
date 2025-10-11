import requests  # type: ignore
from logger import logger
from bs4 import BeautifulSoup  # type: ignore
from csv_handelling import return_link
from bs4.element import Comment  # type: ignore


def scrape_website() :
    url = return_link()
    if not url:
        logger.warning("No valid URL returned by return_link().")
        return None
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all([
            'script', 'style', 'noscript', 'iframe', 'link', 'img', 'picture', 'meta',
            'button', 'svg', 'form', 'header', 'footer', 'head', 'a','table','h4',
            'figure','h5','h6'
        ]):
            tag.decompose()
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
        for _ in range(3):
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
        return soup
    except requests.exceptions.RequestException as e:
        logger.warning(f"Error scraping {url}: {e}")
        return None
        
        
def section_maker():        
        soup = scrape_website()
        if soup is not None:
            sections = {}
            index = 1
            for tag in soup.find_all(['section']): 
                    text = str(tag)
                    if not text:
                        continue
                    if len(text.split()) < 50:
                        continue
                    if not text.startswith("<section><h2>"):
                        continue
                    sections[str(index)] = text
                    index += 1
            return sections
        else:
            return  

def final_data():
    data = section_maker()
    if not data:
        return ""

    bad_words = [
        "Acknowledgements", "References", "Authors' contributions",
        "Supplementary Material", "Associated Data","Funding"
    ]

    filtered = {
        k: v
        for k, v in data.items()
        if not any(bw.lower() in str(v).lower() for bw in bad_words)
    }

    logger.info("Removed Noise from recieved data and sent it for formatting")
    return "\n\n\n======================\n\n\n".join(filtered.values())


