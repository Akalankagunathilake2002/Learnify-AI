# app/core/gemini_client.py
import os
from typing import Optional, Tuple
from google import genai  # pip install google-genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def _client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")
    return genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini_text(prompt: str, model: str = "gemini-2.5-flash") -> str:
    client = _client()
    resp = client.models.generate_content(model=model, contents=[prompt])

    text = getattr(resp, "text", None)
    if text:
        return text.strip()

    parts = getattr(resp, "parts", None) or []
    out = []
    for part in parts:
        if getattr(part, "text", None):
            out.append(part.text)
    return "\n".join(out).strip()

def generate_gemini_image(
    prompt: str,
    model: str = "gemini-2.5-flash-image"
) -> Tuple[Optional[str], Optional[str], str]:
    """
    Returns: (image_base64, mime, any_text)
    """
    client = _client()
    resp = client.models.generate_content(model=model, contents=[prompt])

    img_b64 = None
    img_mime = None
    texts = []

    for part in getattr(resp, "parts", []) or []:
        if getattr(part, "text", None):
            texts.append(part.text)
        elif getattr(part, "inline_data", None) is not None:
            inline = part.inline_data
            img_b64 = getattr(inline, "data", None)
            img_mime = getattr(inline, "mime_type", None) or "image/png"

    return img_b64, img_mime, ("\n".join(texts).strip())
