from datetime import datetime, timezone

import stripe
from app.model.organization_model import Organization
from stripe import Event, Webhook, billing_portal, checkout
from stripe import error as stripe_error


class StripeService:
    def __init__(self, api_key: str, webhook_secret):
        stripe.api_key = api_key
        self.webhook_secret = webhook_secret

    def create_customer(
        self, *, email: str, name: str, metadata: dict
    ) -> stripe.Customer:
        return stripe.Customer.create(email=email, name=name, metadata=metadata)

    def list_prices_for_product(self, product_id: str) -> list[stripe.Price]:
        prices = stripe.Price.list(
            product=product_id,
            active=True,
            expand=["data.product"],
        )
        return prices.data

    def create_free_subscription(
        self, customer_id: str, price_id: str
    ) -> stripe.Subscription:
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
        )

    def extract_subscription_details(self, subscription: stripe.Subscription) -> dict:
        item = subscription["items"]["data"][0]
        return {
            "subscription_id": subscription.id,
            "customer_id": subscription.customer,
            "status": subscription.status,
            "product_id": item["price"]["product"],
            "period_start": datetime.fromtimestamp(
                item["current_period_start"], tz=timezone.utc
            ),
            "period_end": datetime.fromtimestamp(
                item["current_period_end"], tz=timezone.utc
            ),
        }

    def create_portal_session(self, customer_id: str, return_url: str) -> str:
        try:
            session = billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            return session.url
        except stripe_error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    def create_checkout_session(
        self, customer_id: str, product_id: str, return_base_url: str
    ) -> str:
        try:
            session = checkout.Session.create(
                mode="subscription",
                customer=customer_id,
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product": product_id,
                            "unit_amount": 0,  # assumed for free checkout
                        },
                        "quantity": 1,
                    }
                ],
                success_url=f"{return_base_url}/dashboard?checkout=success",
                cancel_url=f"{return_base_url}/dashboard?checkout=cancel",
            )
            return session.url
        except stripe_error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    def parse_event(self, payload: bytes, sig_header: str) -> Event:
        try:
            return Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=self.webhook_secret,
            )
        except ValueError as e:
            raise ValueError(f"Invalid payload: {e}")
        except stripe_error.SignatureVerificationError as e:
            raise ValueError(f"Invalid signature: {e}")
