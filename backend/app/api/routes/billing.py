import os
import stripe
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.auth import get_current_user
from app.db.deps import get_db
from app.models.user import User

router = APIRouter(prefix="/billing", tags=["billing"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


@router.post("/create-checkout-session")
def create_checkout_session(user: User = Depends(get_current_user)):
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


@router.get("/sync-success")
def sync_success(
    session_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Called by frontend on /billing/success page.
    Verifies the Stripe session, and updates DB so /users/me returns is_premium=true.
    """
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")

    try:
        sess = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid session_id: {e}")

    # ✅ Security: ensure session belongs to this user
    metadata = sess.get("metadata") or {}
    if str(metadata.get("user_id")) != str(user.id):
        raise HTTPException(status_code=403, detail="Session does not belong to this user")

    # ✅ Check subscription exists
    subscription_id = sess.get("subscription")
    customer_id = sess.get("customer")

    if not subscription_id:
        raise HTTPException(status_code=400, detail="No subscription found in session")

    # ✅ Update DB
    db_user = db.execute(select(User).where(User.id == user.id)).scalar_one()
    db_user.is_premium = True
    db_user.stripe_customer_id = customer_id
    db_user.stripe_subscription_id = subscription_id
    db.commit()

    return {"ok": True, "is_premium": True}
