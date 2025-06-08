# scraping/scraper_core.py

import time
import requests
from bs4 import BeautifulSoup
from newspaper import Article

from config.settings import DJANGO_API_ENDPOINT, KEYWORDS, SCRAPE_INTERVAL_SECONDS
from scrapping.sources import FASHION_SOURCES
from utils.deduplication import (
    load_scraped_urls, save_scraped_url,
    load_processed_hashes, save_processed_hash,
    get_text_hash
)
from utils.image_fetcher import fetch_image_from_article
from nlp_pipeline.sentiment import analyze_sentiment
from nlp_pipeline.ner import extract_entities
from nlp_pipeline.topic_classifier import classify_topic
from nlp_pipeline.summarizer import smart_summarize


def scrape_fashion_articles():
    articles = []

    for source_name, base_url in FASHION_SOURCES.items():
        try:
            response = requests.get(base_url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")

            for a_tag in soup.select("a[href]"):
                link = a_tag.get("href")
                if not link:
                    continue
                if not link.startswith("http"):
                    link = base_url.rstrip("/") + "/" + link.lstrip("/")
                text = a_tag.get_text(strip=True)

                if text and any(k in link.lower() or k in text.lower() for k in KEYWORDS):
                    articles.append((text, link))

        except Exception as e:
            print(f"❌ Error scraping {source_name}: {e}")

    unique = list({url: (title, url) for title, url in articles}.values())
    return unique


def fetch_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        print(article.text)
        return article.title, article.text
    except Exception as e:
        print(f"❌ Error parsing article: {e}")
        return None, None


def process_article(title, url, text):
    sentiment = analyze_sentiment(text)
    entities = extract_entities(text)
    topic = classify_topic(text)
    summary = smart_summarize(text)
    image_url = fetch_image_from_article(url)

    return {
        "title": title,
        "url": url,
        "summary": summary,
        "sentiment": sentiment["label"],
        "sentiment_score": sentiment["score"],
        "entities": {e: [e] for e in entities},
        "topic": topic["label"],
        "score": topic["score"],
        "image_url": image_url,
    }


def send_to_api(payload):
    try:
        r = requests.post(DJANGO_API_ENDPOINT, json=payload)
        if r.status_code in [200, 201]:
            print(f"✅ Sent: {payload['title']}")
        else:
            print(f"⚠️ API error: {r.status_code} {r.text}")
    except Exception as e:
        print(f"❌ Error sending to API: {e}")


def process_real_time_news():
    scraped_urls = load_scraped_urls()
    processed_hashes = load_processed_hashes()

    while True:
        print("🔍 Scraping sources...")
        articles = scrape_fashion_articles()

        for title, url in articles:
            if url in scraped_urls:
                print(f"↪️ Skipped (already scraped): {title}")
                continue

            article_title, text = fetch_article_text(url)
            if not text or not any(k in text.lower() for k in KEYWORDS):
                print(f"⛔️ Irrelevant or empty: {title}")
                continue

            content_hash = get_text_hash(text)
            if content_hash in processed_hashes:
                print(f"♻️ Duplicate content: {title}")
                save_scraped_url(url)
                scraped_urls.add(url)
                continue

            print(f"📄 Processing: {article_title}")
            payload = process_article(article_title, url, text)
            send_to_api(payload)

            save_scraped_url(url)
            scraped_urls.add(url)
            save_processed_hash(content_hash)
            processed_hashes.add(content_hash)

        print(f"⏳ Waiting {SCRAPE_INTERVAL_SECONDS}s...\n")
        time.sleep(SCRAPE_INTERVAL_SECONDS)
