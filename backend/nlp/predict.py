import logging
import aiohttp
import asyncio
import json

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ForechainPredictor")

app = FastAPI()

# Configure CORS - allow Angular development server
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chutes AI config
CHUTES_API_KEY = "cpk_3569773a8697471b8cb4a419bfb25e1a.6696cdc860765feda4494828165722ed.aCYxPVuJvvker3RMX3HgVXYxxVsPiSWb"
CHUTES_API_URL = "https://llm.chutes.ai/v1/chat/completions"

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Forechain Prediction API!"}


async def call_chutes_api(prompt: str):
    headers = {
        "Authorization": f"Bearer {CHUTES_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.7,
        "stream": False
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                CHUTES_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            ) as response:
                response_text = await response.text()
                logger.info(f"Chutes API response: {response_text[:300]}...")

                try:
                    resp_json = json.loads(response_text)
                except json.JSONDecodeError:
                    logger.error("Invalid JSON from Chutes API")
                    return {
                        "error": "Invalid JSON response",
                        "status_code": response.status,
                        "raw_response": response_text
                    }

                if response.status != 200:
                    error_msg = resp_json.get("error", {}).get("message", "Unknown error")
                    logger.error(f"API error: {error_msg}")
                    return {
                        "error": "Prediction service error",
                        "details": error_msg,
                        "status_code": response.status
                    }

                if "choices" in resp_json and resp_json["choices"]:
                    prediction = resp_json["choices"][0]["message"]["content"].strip()
                    return {"prediction": prediction}
                else:
                    logger.error("Unexpected response format from Chutes API")
                    return {
                        "error": "No prediction found",
                        "raw_response": resp_json
                    }

    except asyncio.TimeoutError:
        logger.error("Chutes API request timed out")
        return {"error": "Prediction service timeout"}
    except Exception as e:
        logger.exception("Unexpected error calling Chutes API")
        return {"error": "Internal server error", "details": str(e)}


@app.post("/predict/alert/")
async def predict_from_alert(request: Request):
    try:
        data = await request.json()
        article_text = data.get("text", "").strip()

        if not article_text:
            raise HTTPException(status_code=400, detail="No article text provided")

        logger.info(f"Received article for prediction. Length: {len(article_text)} characters.")
 
        truncated_text = article_text[:2000] + ("..." if len(article_text) > 2000 else "")

        prompt = f"""
        You are Forechain, an AI expert in analyzing global news to predict effects on the Philippine fashion supply chain.

        INSTRUCTIONS:
        Analyze the following news article and return a prediction in STRICT JSON format only, with no extra text, explanation, markdown, or preamble. Do NOT include "```json" or any commentary.

        ARTICLE:
        \"\"\"{truncated_text}\"\"\"

        Respond using ONLY this JSON format:

        {{
            "insight": "[One-sentence summary of the predicted impact]",
            "impact_scale": "[Low | Medium | High]",
            "reasoning": "[Brief but logical explanation]",
            "recommendation": {{
                "summary": "[One clear recommendation for PH fashion supply chain stakeholders]",
                "when": "[When to take action]",
                "where": "[Where to seek help or which authorities or participants to involve]",
                "why": "[Why this recommendation is crucial]",
                "how": ["[Step 1]", "[Step 2]", "..."]
            }}
        }}
        """.strip()


        result = await call_chutes_api(prompt)

        if isinstance(result, dict) and result.get("prediction") and isinstance(result["prediction"], str):
            try:
                parsed = json.loads(result["prediction"])
                return parsed
            except json.JSONDecodeError:
                logger.warning("Trying to extract JSON block manually")
                import re
                match = re.search(r'\{.*\}', result["prediction"], re.DOTALL)
                if match:
                    try:
                        return json.loads(match.group())
                    except Exception:
                        logger.error("Fallback JSON extraction failed")
                raise HTTPException(
                    status_code=502,
                    detail="Model returned malformed JSON",
                )
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Unknown error from prediction service")
            )

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.exception("Unhandled error in predict_from_alert")
        raise HTTPException(status_code=500, detail=str(e))