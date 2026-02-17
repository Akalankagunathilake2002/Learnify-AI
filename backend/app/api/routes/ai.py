from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.models.user import User

from app.core.groq_client import ask_groq
from app.core.gemini_client import ask_gemini_text, generate_gemini_image

router = APIRouter(prefix="/ai", tags=["ai"])

class AskReq(BaseModel):
    question: str
    provider: str = "groq"   # groq | gemini
    task: str = "tutor"      # tutor | notes | image

@router.post("/ask")
def ask_ai(payload: AskReq, user: User = Depends(get_current_user)):
    if not user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")

    q = (payload.question or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question is required")

    provider = (payload.provider or "groq").lower()
    task = (payload.task or "tutor").lower()

    # ✅ NOTES
    if task == "notes":
        prompt = (
            "Create clear study notes.\n"
            "Include: short explanation, key points, simple example, and 5 MCQs with answers.\n\n"
            f"Topic: {q}"
        )
        answer = ask_gemini_text(prompt) if provider == "gemini" else ask_groq(prompt)
        return {"answer": answer, "provider": provider, "task": task}

    # ✅ IMAGE (Gemini only)
    if task == "image":
        if provider != "gemini":
            raise HTTPException(status_code=400, detail="Image generation only works with Gemini")

        img_b64, img_mime, txt = generate_gemini_image(q)
        if not img_b64:
            raise HTTPException(status_code=500, detail="Gemini did not return an image")

        return {
            "answer": txt or "✅ Image generated",
            "provider": provider,
            "task": task,
            "image_base64": img_b64,
            "image_mime": img_mime or "image/png",
        }

    # ✅ TUTOR default
    prompt = f"Explain simply with a small example:\n\n{q}"
    answer = ask_gemini_text(prompt) if provider == "gemini" else ask_groq(prompt)
    return {"answer": answer, "provider": provider, "task": task}
