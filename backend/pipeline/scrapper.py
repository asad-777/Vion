import requests  # type: ignore
from logger import logger
from bs4 import BeautifulSoup, NavigableString, Tag  # type: ignore
from csv_handelling import return_link
from bs4.element import Comment  # type: ignore
import re



def traverse(node):
    """Recursively extract text in order, keeping headings and sub/sup."""
    result = []
    if isinstance(node, NavigableString):
        text = node.strip()
        if text:
            result.append(text)
    elif isinstance(node, Tag):
        if node.name in ['h2']:
            text = node.get_text(strip=True)
            if text:
                result.append(f"\n# {text}\n")
        elif node.name in ['h3']:
            text = node.get_text(strip=True)
            if text:
                result.append(f"\n### {text}\n")
        elif node.name in ['sub', 'sup']:
            result.append(str(node))
        else:
            for child in node.children:
                result.extend(traverse(child))
    combined = "".join(result)
    return combined

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
                    
                    tags_to_remove = ['section', 'p', 'em', 'strong','span']
                    pattern = r'</?(?:' + '|'.join(tags_to_remove) + r')>'
                    clean_text = re.sub(pattern, '', text, flags=re.IGNORECASE)
                    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                    soup_traverse = BeautifulSoup(clean_text, "html.parser")
                    clean_clean_text = traverse(soup_traverse)
                    sections[str(index)] = clean_clean_text
                    index += 1
            return sections
        else:
            logger.warning("Nothing to make sections of")
            return  None

def final_data():
    data = section_maker()
    if not data:
        logger.info("No data to return bad words from")
        return ""

    bad_words = [
        "Acknowledgements","Acknowledgments", "References", "Authors' contributions",
        "Supplementary Material", "Associated Data","Funding"
    ]

    filtered = {
        k: v
        for k, v in data.items()
        if not any(bw.lower() in str(v).lower() for bw in bad_words)
    }

    logger.info("Removed Noise from recieved data and sent it for formatting")
    return "\n\n".join(filtered.values())


