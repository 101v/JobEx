import requests
from bs4 import BeautifulSoup
from jobex.strana import simple_match, key_words
from jobex.db import dbhelper

class TextBlock:
    def __init__(self, root_element) -> None:
        self.root_element = root_element
        self.text = ""
        self.length = 0
        self.relative_length_percentage = 0
        self.words_of_interest = []
        self.tech_keywords = []

    def append_text(self, text: str):
        if text:
            text = " ".join(text.split())
            self.text = (self.text + " " + text.lower()).strip()
            self.length = len(self.text)

class WebPage:
    def __init__(self, url, soup) -> None:
        self.url = url
        self.soup = soup
        self.page_content = soup.prettify() if soup else ""
        self.text_blocks = []
        self.tech_keywords = []

    def extract_text_blocks(self):
        if len(self.text_blocks) > 0:
            return
        
        divs = self.soup.find_all('div')
        for d in divs:
            block_text = TextBlock(d)
            # get text elements directly inside div
            text = " ".join(d.find_all(text=True, recursive=False))
            block_text.append_text(text)

            for child in d.children:
                if child.name == "h1" or child.name == "h2" or child.name == "h3" or child.name == "h4" or child.name == "h5" or child.name == "h6":
                    block_text.append_text(child.get_text())
                    
                if child.name == "p":
                    block_text.append_text(child.get_text())
                    
                if child.name == "ul" or child.name == "ol":
                    for item in child.find_all("li", recursive=False):
                        block_text.append_text(item.get_text())

            if block_text.length > 0:           
                self.text_blocks.append(block_text)

        self.calculate_relative_length()

    def calculate_relative_length(self):
        if len(self.text_blocks) == 0:
            return

        longest_block = max(self.text_blocks, key=lambda item: item.length)
        longest_block.relative_length_percentage = 100

        if longest_block.length == 0:
            return

        for tb in self.text_blocks:
            tb.relative_length_percentage = (tb.length/longest_block.length) * 100

    def match_tech_keywords(self):
        tech_keywords = []
        for tb in self.text_blocks:
            if tb.relative_length_percentage >= 49.99:
                tokens = simple_match.tokenize(tb.text)
                tb.tech_keywords = simple_match.find_matches(tokens, key_words.tech_keywords_candidates)
                tech_keywords = tech_keywords + tb.tech_keywords
        
        self.tech_keywords = list(set(tech_keywords))
    
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

def get_webpage_soup(url: str) -> WebPage:
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    return WebPage(url, soup)

def analyze_webpage(url, tweet_source_id):
    max_retry = 3
    i = 0
    is_complete = False
    webpage = WebPage("", None)
    error_text = ""
    while i < max_retry and not is_complete:
        i = i + 1
        try:
            webpage = get_webpage_soup(url)
            webpage.extract_text_blocks()
            webpage.match_tech_keywords()
            
            is_complete = True
        except BaseException as e:
            error_text = str(e)

    if is_complete:
        error_text = ""

    dbhelper.insert_page(webpage.page_content, webpage.tech_keywords, webpage.url, tweet_source_id, error_text)


