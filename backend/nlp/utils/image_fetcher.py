import requests
from bs4 import BeautifulSoup

def fetch_image_from_article(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        # Try to get og:image meta tag
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
        # Fallback: find first <img> tag
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            return img_tag["src"]
        return None
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None
