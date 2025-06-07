from transformers import pipeline
from config.settings import FASHION_TOPICS

topic_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_topic(text):
    try:
        result = topic_classifier(text[:512], candidate_labels=FASHION_TOPICS)
        return {"label": result["labels"][0], "score": result["scores"][0]}
    except Exception as e:
        print(f"[Topic Classification] Error: {e}")
        return {"label": "Unknown", "score": 0}
