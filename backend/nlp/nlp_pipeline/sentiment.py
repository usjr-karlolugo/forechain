from transformers import pipeline, DistilBertTokenizer, DistilBertForSequenceClassification

# Load sentiment pipeline
sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = DistilBertTokenizer.from_pretrained(sentiment_model_name)
model = DistilBertForSequenceClassification.from_pretrained(sentiment_model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def analyze_sentiment(text):
    max_length = 512
    chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    sentiment_scores = {"positive": [], "negative": [], "neutral": []}

    for chunk in chunks:
        result = sentiment_pipeline(chunk)[0]
        label = result["label"].lower()
        score = result["score"]

        if 0.45 <= score <= 0.55:
            sentiment_scores["neutral"].append(score)
        else:
            sentiment_scores[label].append(score)

    avg_scores = {
        cat: (sum(scores) / len(scores) if scores else 0)
        for cat, scores in sentiment_scores.items()
    }
    final_label = max(avg_scores, key=avg_scores.get)
    return {"label": final_label, "score": avg_scores[final_label]}
