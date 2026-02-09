from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user
from app.core.groq_client import ask_groq
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/ask")
def ask_ai(payload: dict, user: User = Depends(get_current_user)):
    # 🔒 Premium check
    if not user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")

    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        answer = ask_groq(question)
        return {"answer": answer}
    except Exception as e:
        # show readable error in backend logs + API
        raise HTTPException(status_code=500, detail=str(e))
