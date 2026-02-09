import os
from groq import Groq

# ✅ pick a supported model (fast + good)
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def ask_groq(question: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing in your backend .env")

    client = Groq(api_key=api_key)

    resp = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful tutor. Explain simply with examples."},
            {"role": "user", "content": question},
        ],
        temperature=0.4,
    )

    return resp.choices[0].message.content or ""
