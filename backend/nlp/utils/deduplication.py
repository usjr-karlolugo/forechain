import os
import hashlib

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
SCRAPED_URLS_FILE = os.path.join(DATA_DIR, 'scraped_urls.txt')
PROCESSED_HASHES_FILE = os.path.join(DATA_DIR, 'processed_hashes.txt')

def load_scraped_urls():
    if os.path.exists(SCRAPED_URLS_FILE):
        with open(SCRAPED_URLS_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_scraped_url(url):
    with open(SCRAPED_URLS_FILE, "a") as f:
        f.write(url + "\n")

def load_processed_hashes():
    if os.path.exists(PROCESSED_HASHES_FILE):
        with open(PROCESSED_HASHES_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_processed_hash(h):
    with open(PROCESSED_HASHES_FILE, "a") as f:
        f.write(h + "\n")

def get_text_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
