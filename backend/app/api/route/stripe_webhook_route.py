import logging

from app.config.container import Container
from app.service.stripe_service import StripeService
from app.service.subscription_service import SubscriptionService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, Response, status

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/stripe", status_code=status.HTTP_200_OK)
@inject
async def stripe_webhook(
    request: Request,
    stripe_service: StripeService = Depends(Provide[Container.stripe_service]),
    subscription_service: SubscriptionService = Depends(
        Provide[Container.subscription_service]
    ),
):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe_service.parse_event(payload, sig_header)
    except ValueError as e:
        logger.error(str(e))
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    event_type = event["type"]

    if event_type in {
        "customer.subscription.created",
        "customer.subscription.updated",
    }:
        await subscription_service.handle_subscription_event(event)

    elif event_type == "customer.subscription.deleted":
        await subscription_service.handle_subscription_cancelled(event.data.object)

    return Response(status_code=status.HTTP_200_OK)
