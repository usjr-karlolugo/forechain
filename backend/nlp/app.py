from flask import Flask, request, jsonify
from nlp.scraper import fetch_news_article, analyze_text  # Import from pipeline.py

app = Flask(__name__)


@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    title, text = fetch_news_article(url)
    if not text:
        return jsonify({"error": "Failed to fetch article"}), 500

    analysis = analyze_text(text[:500])  # Limit text length
    return jsonify({"title": title, "analysis": analysis})


if __name__ == "__main__":
    app.run(debug=True)
