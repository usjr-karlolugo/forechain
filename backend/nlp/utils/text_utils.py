import re
from bs4 import BeautifulSoup

def clean_html(raw_html: str) -> str:
    return BeautifulSoup(raw_html, "html.parser").get_text()

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()