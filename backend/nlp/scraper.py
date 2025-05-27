import os
import time
import requests
import hashlib
from bs4 import BeautifulSoup
from newspaper import Article
from transformers import (
    pipeline,
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=r"C:\Users\Miguel\forechain\backend\nlp\x.env")

# API endpoint
DJANGO_API_ENDPOINT = os.getenv(
    "DJANGO_API_ENDPOINT", "http://127.0.0.1:8000/api/alerts/"
)
if not DJANGO_API_ENDPOINT:
    print("❌ Missing Django API Endpoint")
    exit(1)

# Sentiment analysis pipeline
sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = DistilBertTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = DistilBertForSequenceClassification.from_pretrained(
    sentiment_model_name
)
sentiment_pipeline = pipeline(
    "sentiment-analysis", model=sentiment_model, tokenizer=tokenizer
)

# Named Entity Recognition pipeline
ner_pipeline = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    aggregation_strategy="simple",
)

# Fashion topic classification
fashion_topic_labels = [
    "Supply Chain",
    "Retail",
    "Design",
    "Sustainability",
    "Marketing",
    "E-Commerce",
    "Innovation",
]
fashion_topic_classifier = pipeline(
    "zero-shot-classification", model="facebook/bart-large-mnli"
)

# Keywords for filtering articles
keywords = [
    "supply chain",
    "shipping",
    "port",
    "freight",
    "demand",
    "fashion",
    "clothing",
    "bags",
    "retail",
    "e-commerce",
]

# --- Deduplication helpers ---


def load_scraped_urls():
    if os.path.exists("scraped_urls.txt"):
        with open("scraped_urls.txt", "r") as file:
            return set(file.read().splitlines())
    return set()


def save_scraped_url(url):
    with open("scraped_urls.txt", "a") as file:
        file.write(url + "\n")


def load_processed_hashes():
    if os.path.exists("processed_hashes.txt"):
        with open("processed_hashes.txt", "r") as f:
            return set(f.read().splitlines())
    return set()


def save_processed_hash(article_hash):
    with open("processed_hashes.txt", "a") as f:
        f.write(article_hash + "\n")


def get_text_hash(text):
    # Normalize text before hashing
    normalized_text = text.strip().lower()
    return hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()


def fetch_news_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title, article.text
    except Exception as e:
        print(f"Error fetching article: {e}")
        return None, None


def analyze_sentiment(text):
    max_length = 512
    chunks = [text[i : i + max_length] for i in range(0, len(text), max_length)]
    sentiment_scores = {"positive": [], "negative": [], "neutral": []}

    for chunk in chunks:
        sentiment = sentiment_pipeline(chunk)[0]
        label = sentiment["label"].lower()
        if 0.45 <= sentiment["score"] <= 0.55:
            sentiment_scores["neutral"].append(sentiment["score"])
        else:
            sentiment_scores[label].append(sentiment["score"])

    avg_scores = {
        category: (sum(scores) / len(scores) if scores else 0)
        for category, scores in sentiment_scores.items()
    }
    final_sentiment = max(avg_scores, key=avg_scores.get)
    return {"label": final_sentiment, "score": avg_scores[final_sentiment]}


def extract_entities(text, entity_labels=None):
    try:
        raw_entities = ner_pipeline(text)
        entities = []
        for ent in raw_entities:
            if "word" in ent and (
                not entity_labels or ent["entity_group"] in entity_labels
            ):
                entities.append(ent["word"].replace(" ##", "").strip())
        return list(set(entities))
    except Exception as e:
        print(f"Error during NER extraction: {e}")
        return []


def classify_topic(text):
    try:
        result = fashion_topic_classifier(
            text[:512], candidate_labels=fashion_topic_labels
        )
        return {"label": result["labels"][0], "score": result["scores"][0]}
    except Exception as e:
        print(f"Error classifying topic: {e}")
        return {"label": "Unknown", "score": 0}


def send_alert_to_api(title, url, sentiment, entities, topic):
    data = {
        "title": title,
        "url": url,
        "sentiment": sentiment["label"],
        "sentiment_score": sentiment["score"],
        "entities": {entity: [entity] for entity in entities},
        "topic": topic["label"],
        "score": topic["score"],
    }
    try:
        response = requests.post(DJANGO_API_ENDPOINT, json=data)
        if response.status_code in [200, 201]:
            print(f"✅ Alert sent to API: {title}")
        else:
            print(f"⚠️ Failed to send alert: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Error sending to API: {e}")


def scrape_fashion_news():
    articles = []

    sources = {
        "Vogue Business": "https://www.voguebusiness.com/",
        "Fashionista": "https://fashionista.com/",
        "Business of Fashion": "https://www.businessoffashion.com/",
        "WWD": "https://wwd.com/",
        "Fashion Network": "https://us.fashionnetwork.com/",
        "Elle": "https://www.elle.com/fashion/",
        "Adobo Magazine": "https://www.adobomagazine.com/fashion/",
        "Philstar": "https://www.philstar.com/lifestyle/fashion-and-beauty",
    }

    for source, url in sources.items():
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.content, "html.parser")
            for a_tag in soup.select("a[href]"):
                link = a_tag.get("href")
                if not link:
                    continue
                if not link.startswith("http"):
                    link = url.rstrip("/") + "/" + link.lstrip("/")
                text = a_tag.get_text(strip=True)
                if text and any(
                    k in link.lower() or k in text.lower() for k in keywords
                ):
                    articles.append((text, link))
        except Exception as e:
            print(f"Error scraping {source}: {e}")

    # Deduplicate by URL
    unique_articles = list({url: (title, url) for title, url in articles}.values())
    return unique_articles


def process_real_time_news():
    scraped_urls = load_scraped_urls()
    processed_hashes = load_processed_hashes()

    while True:
        print("🔍 Scraping fashion news sources...")
        articles = scrape_fashion_news()

        for title, url in articles:
            if url in scraped_urls:
                print(f"⚠️ Already scraped URL: {title}")
                continue

            article_title, article_text = fetch_news_article(url)
            if not article_text:
                print(f"⚠️ Could not fetch content: {title}")
                continue

            # Content hash deduplication
            article_hash = get_text_hash(article_text)
            if article_hash in processed_hashes:
                print(f"⚠️ Duplicate article content detected: {title}")
                # Mark URL scraped anyway to avoid repeated attempts
                save_scraped_url(url)
                scraped_urls.add(url)
                continue

            if not any(k in article_text.lower() for k in keywords):
                print(f"⛔️ Irrelevant content: {title}")
                continue

            print(f"--- Analyzing: {article_title} ---")
            sentiment = analyze_sentiment(article_text)
            entities = extract_entities(article_text)
            topic = classify_topic(article_text)
            send_alert_to_api(article_title, url, sentiment, entities, topic)

            save_scraped_url(url)
            scraped_urls.add(url)

            save_processed_hash(article_hash)
            processed_hashes.add(article_hash)

        print("⏳ Waiting 10 seconds before next scrape...\n")
        time.sleep(10)


if __name__ == "__main__":
    process_real_time_news()
