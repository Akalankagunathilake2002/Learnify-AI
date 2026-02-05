import os
import stripe
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout_session(
    *,
    customer_email: str,
    price_id: str,
    success_url: str,
    cancel_url: str,
):
    """
    Creates a Stripe Checkout Session for subscriptions
    """
    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        customer_email=customer_email,
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
    )

    return session.url
