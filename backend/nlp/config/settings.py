import os
from dotenv import load_dotenv

# Load .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Django API Endpoint
DJANGO_API_ENDPOINT = os.getenv("DJANGO_API_ENDPOINT", "http://127.0.0.1:8000/api/alerts/")

# Keywords used for filtering relevant articles
KEYWORDS = [
    "supply chain", "shipping", "port", "freight", "demand",
    "fashion", "clothing", "bags", "retail", "e-commerce"
]

# Fashion topic labels
FASHION_TOPICS = [
    "Supply Chain", "Retail", "Design", "Sustainability",
    "Marketing", "E-Commerce", "Innovation"
]

# Scraping frequency
SCRAPE_INTERVAL_SECONDS = 10
