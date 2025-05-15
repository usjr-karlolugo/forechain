import requests
from fastapi import FastAPI, Request
import logging

app = FastAPI()
DEEPSEEK_API_KEY = "sk-97fbd74b67d643eca71c1988a06660d7"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


@app.post("/predict/")
async def predict_alert(request: Request):
    try:
        data = await request.json()
        title = data.get("title", "")
        topic = data.get("topic", "")
        sentiment = data.get("sentiment", "")

        prompt = f"""
        Analyze this alert and predict its possible impact on the Philippine supply chain:
        Title: {title}
        Topic: {topic}
        Sentiment: {sentiment}
        """

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "deepseek-llama2-7b-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }

        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)

        # Debug print/log everything
        logging.warning(f"Status: {response.status_code}")
        logging.warning(f"Response: {response.text}")

        # Try to parse JSON
        try:
            result = response.json()
            prediction = result["choices"][0]["message"]["content"].strip()
            return {"prediction": prediction}
        except Exception as json_error:
            return {
                "error": "Failed to parse DeepSeek response.",
                "details": str(json_error),
                "status_code": response.status_code,
                "raw_response": response.text,
            }

    except Exception as e:
        return {"error": "Something went wrong in the backend.", "details": str(e)}
