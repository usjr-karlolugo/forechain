import requests
from nlp.config.settings import DJANGO_API_ENDPOINT

def send_alert_to_api(title, url, sentiment, entities, topic, summary, image_url=None):
    data = {
        "title": title,
        "url": url,
        "sentiment": sentiment["label"],
        "sentiment_score": sentiment["score"],
        "entities": {entity: [entity] for entity in entities},
        "topic": topic["label"],
        "score": topic["score"],
        "summary": summary,
        "image_url": image_url,
    }

    try:
        response = requests.post(DJANGO_API_ENDPOINT, json=data)
        if response.status_code in [200, 201]:
            print(f"✅ Alert sent to API: {title}")
        else:
            print(f"⚠️ Failed to send alert: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Error sending to API: {e}")