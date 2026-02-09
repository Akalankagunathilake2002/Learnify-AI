import os
import stripe
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.deps import get_db
from app.models.user import User

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

@router.post("/stripe", response_model=None)
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Stripe webhook secret not set")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        metadata = data.get("metadata") or {}
        user_id_raw = metadata.get("user_id")

        customer_id = data.get("customer")
        subscription_id = data.get("subscription")

        if user_id_raw:
            user_id = int(user_id_raw)
            user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
            if user:
                user.is_premium = True
                user.stripe_customer_id = customer_id
                user.stripe_subscription_id = subscription_id
                db.commit()

    elif event_type == "invoice.paid":
        subscription_id = data.get("subscription")
        if subscription_id:
            user = db.execute(
                select(User).where(User.stripe_subscription_id == subscription_id)
            ).scalar_one_or_none()
            if user:
                user.is_premium = True
                db.commit()

    elif event_type in ("customer.subscription.deleted", "customer.subscription.updated"):
        sub_id = data.get("id")
        sub_status = data.get("status")

        if sub_id:
            user = db.execute(
                select(User).where(User.stripe_subscription_id == sub_id)
            ).scalar_one_or_none()
            if user and sub_status in ("canceled", "unpaid", "incomplete_expired"):
                user.is_premium = False
                db.commit()

    return {"ok": True}
