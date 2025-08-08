import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in your environment.")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

def get_advice_from_groq(conditions):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a medical assistant. Provide short bullet-point care advice (1–2 points per condition). "
                    "If urgent, say 'See doctor immediately'."
                )
            },
            {
                "role": "user",
                "content": f"Conditions: {', '.join(conditions)}"
            }
        ],
        "temperature": 0.4,
        "max_tokens": 250
    }

    resp = requests.post(GROQ_URL, headers=headers, json=payload)
    resp.raise_for_status()
    result = resp.json()

    try:
        return result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        return "No advice returned."

if __name__ == "__main__":
    print(get_advice_from_groq(["fever", "cough"]))
