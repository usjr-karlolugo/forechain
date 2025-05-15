import os
import time
import requests
from newspaper import Article
from transformers import (
    pipeline,
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=r"C:\Users\Miguel\forechain\backend\nlp\x.env")

# API keys and endpoints
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DJANGO_API_ENDPOINT = os.getenv(
    "DJANGO_API_ENDPOINT", "http://127.0.0.1:8000/api/alerts/"
)  # Fixed this line

# Check for missing API keys
if not NEWS_API_KEY:
    print("❌ Missing News API Key")
    exit(1)

if not DJANGO_API_ENDPOINT:
    print("❌ Missing Django API Endpoint")
    exit(1)

# Load pre-trained sentiment analysis model
sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = DistilBertTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = DistilBertForSequenceClassification.from_pretrained(
    sentiment_model_name
)

# Set up NLP pipelines
sentiment_pipeline = pipeline(
    "sentiment-analysis", model=sentiment_model, tokenizer=tokenizer
)
ner_pipeline = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    aggregation_strategy="simple",
)
topic_classifier = pipeline(
    "text-classification",
    model="mrm8488/bert-mini-finetuned-age_news-classification",
    tokenizer="mrm8488/bert-mini-finetuned-age_news-classification",
)

# Define keywords
keywords = [
    "supply chain disruption",
    "shipping delays",
    "port congestion",
    "freight disruption",
    "supply",
    "demand",
]


# Store processed URLs to avoid redundant scraping (file-based approach)
def load_scraped_urls():
    if os.path.exists("scraped_urls.txt"):
        with open("scraped_urls.txt", "r") as file:
            return set(file.read().splitlines())
    return set()


def save_scraped_url(url):
    with open("scraped_urls.txt", "a") as file:
        file.write(url + "\n")


# Fetch articles from News API
def fetch_articles():
    url = f"https://newsapi.org/v2/everything?q=supply+chain&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles: {e}")
        return []


# Fetch and parse a news article
def fetch_news_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title, article.text
    except Exception as e:
        print(f"Error fetching article: {e}")
        return None, None


# NLP functions with chunking for long texts
def analyze_sentiment(text):
    max_length = 512  # Model's token limit
    chunks = [text[i : i + max_length] for i in range(0, len(text), max_length)]
    sentiment_scores = {"positive": [], "negative": [], "neutral": []}

    for chunk in chunks:
        sentiment = sentiment_pipeline(chunk)[0]
        label = sentiment["label"].lower()

        # If the score is close to 0.5, classify it as neutral
        if 0.45 <= sentiment["score"] <= 0.55:
            sentiment_scores["neutral"].append(sentiment["score"])
        else:
            sentiment_scores[label].append(sentiment["score"])

    # Compute average scores
    avg_scores = {
        category: (sum(scores) / len(scores) if scores else 0)
        for category, scores in sentiment_scores.items()
    }

    # Determine final sentiment based on the highest average score
    final_sentiment = max(avg_scores, key=avg_scores.get)

    return {"label": final_sentiment, "score": avg_scores[final_sentiment]}


def extract_entities(text, entity_labels=None):
    """
    Extract and group named entities from text using the NER pipeline.

    Parameters:
        text (str): The input text to analyze.
        entity_labels (list): Optional list of entity types to include (e.g., ["ORG", "LOC"]).

    Returns:
        List of unique entity strings.
    """
    try:
        raw_entities = ner_pipeline(text)
        entities = []

        for ent in raw_entities:
            if "word" not in ent:
                continue
            if entity_labels and ent["entity_group"] not in entity_labels:
                continue
            clean_word = ent["word"].replace(" ##", "").strip()
            entities.append(clean_word)

        return list(set(entities))  # Remove duplicates

    except Exception as e:
        print(f"Error during NER extraction: {e}")
        return []


def classify_topic(text):
    try:
        result = topic_classifier(text[:512])[0]
        label_map = {
            "LABEL_0": "World",
            "LABEL_1": "Sports",
            "LABEL_2": "Business",
            "LABEL_3": "Sci/Tech",
        }
        return {
            "label": label_map.get(result["label"], "Unknown"),
            "score": result["score"],
        }
    except Exception as e:
        print(f"Error classifying topic: {e}")
        return {"label": "Unknown", "score": 0}


# Send alert to Django backend
def send_alert_to_api(title, url, sentiment, entities, topic):
    # Convert entities list to a dictionary with entity names as keys, and values as a list of items (e.g., [entity, entity, ...])
    entities_dict = {
        entity: [entity] for entity in entities
    }  # List of entities as items

    result = topic_classifier(title)[0]
    data = {
        "title": title,
        "url": url,
        "sentiment": sentiment["label"],
        "sentiment_score": sentiment["score"],
        "entities": entities_dict,
        "topic": result["label"],
        "score": result["score"],
    }

    try:
        response = requests.post(DJANGO_API_ENDPOINT, json=data)
        if response.status_code in [200, 201]:
            print(f"✅ Alert sent to API: {title}")
        else:
            print(f"⚠️ Failed to send alert: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Error sending to API: {e}")


# Process and send alerts
def process_real_time_news():
    scraped_urls = load_scraped_urls()  # Load previously scraped URLs
    while True:
        articles = fetch_articles()
        for article in articles:
            title = article["title"]
            url = article["url"]
            description = article.get("description", "")

            if url in scraped_urls:
                print(f"⚠️ Skipping already scraped article: {title}")
                continue

            if description and any(k in description.lower() for k in keywords):
                print(f"--- Analyzing Article: {title} ---")
                article_title, article_text = fetch_news_article(url)
                if article_text:
                    sentiment = analyze_sentiment(article_text)
                    entities = extract_entities(article_text)
                    topic = classify_topic(article_text)
                    send_alert_to_api(title, url, sentiment, entities, topic)

                # Save the URL to avoid scraping again
                save_scraped_url(url)
                scraped_urls.add(url)

            if not description:
                print(f"⚠️ Skipping article due to missing description: {title}")
                continue

        print("⏳ Waiting 10 minutes before next check...\n")
        time.sleep(600)


def process_user_provided_news():
    scraped_urls = load_scraped_urls()  # Load previously scraped URLs

    while True:
        url = input("Enter a news article URL (or type 'exit' to quit): ").strip()
        if url.lower() == "exit":
            break

        if url in scraped_urls:
            print("⚠️ This article has already been processed.")
            continue

        title, text = fetch_news_article(url)
        if not text:
            print("⚠️ Skipping due to fetch error or empty content.")
            continue

        print(f"--- Analyzing Article: {title} ---")
        if any(k in text.lower() for k in keywords):
            sentiment = analyze_sentiment(text)
            entities = extract_entities(text)
            topic = classify_topic(text)
            send_alert_to_api(title, url, sentiment, entities, topic)

            save_scraped_url(url)
            scraped_urls.add(url)
        else:
            print("⚠️ Article doesn't contain relevant keywords. Skipping.")


# Run
if __name__ == "__main__":
    # process_real_time_news()
    process_user_provided_news()
