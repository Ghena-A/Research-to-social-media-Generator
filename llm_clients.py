# llm_clients.py

from openai import OpenAI
import requests
from config import OPENROUTER_API_KEY

# =======================
# OpenRouter
# =======================
openrouter_client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def openrouter_generate(
    prompt,
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=600
):
    response = openrouter_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a professional social media content writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


# =======================
# Ollama (fallback)
# =======================
def ollama_generate(
    prompt,
    model="tinyllama:1.1b-chat",
    temperature=0.6,
    max_tokens=400
):
    r = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        },
        timeout=60
    )

    data = r.json()
    if "message" in data:
        return data["message"]["content"]

    raise RuntimeError(f"Ollama error: {data}")
