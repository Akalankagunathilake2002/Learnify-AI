import os
import stripe
from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user

router = APIRouter(prefix="/billing", tags=["billing"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

@router.post("/create-checkout-session")
def create_checkout_session(user=Depends(get_current_user)):
    if not stripe.api_key or not PRICE_ID:
        raise HTTPException(status_code=500, detail="Stripe not configured")

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": PRICE_ID, "quantity": 1}],
            success_url=f"{FRONTEND_URL}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/billing/cancel",
            customer_email=user.email,
            metadata={"user_id": str(user.id)},
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
