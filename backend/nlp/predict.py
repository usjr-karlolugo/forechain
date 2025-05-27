import requests
import json
import logging
import aiohttp
import asyncio
from fastapi import FastAPI, Request

app = FastAPI()
CHUTES_API_KEY = "cpk_3569773a8697471b8cb4a419bfb25e1a.6696cdc860765feda4494828165722ed.aCYxPVuJvvker3RMX3HgVXYxxVsPiSWb"
CHUTES_API_URL = "https://llm.chutes.ai/v1/chat/completions"


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Forechain Prediction API!"}


@app.post("/predict/")
async def predict_alert(request: Request):
    try:
        data = await request.json()
        title = data.get("title", "")
        topic = data.get("topic", "")
        sentiment = data.get("sentiment", "")

        prompt = f"""
        Analyze this alert and predict its possible impact on the Philippine fashion supply chain:
        Title: {title}
        Topic: {topic}
        Sentiment: {sentiment}
        """

        headers = {
            "Authorization": f"Bearer {CHUTES_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "deepseek-ai/DeepSeek-R1",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1024,
            "temperature": 0.7,
            "stream": False,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                CHUTES_API_URL, headers=headers, json=payload
            ) as response:
                resp_json = await response.json()
                if "choices" in resp_json:
                    prediction = resp_json["choices"][0]["message"]["content"].strip()
                    return {"prediction": prediction}
                elif "error" in resp_json:
                    return {
                        "error": "Chutes API error",
                        "details": resp_json["error"].get("message", "Unknown error"),
                        "status_code": response.status,
                        "raw_response": await response.text(),
                    }
                else:
                    return {
                        "error": "Unexpected Chutes response format.",
                        "status_code": response.status,
                        "raw_response": await response.text(),
                    }
    except Exception as e:
        return {"error": "Something went wrong in the backend.", "details": str(e)}
