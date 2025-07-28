import logging
import time
from datetime import datetime, timezone

from app.config.settings import settings
from app.data.repo.organization_plan_repo import OrganizationPlanRepo
from app.data.repo.organization_repo import OrganizationRepo
from app.data.repo.plan_repo import PlanRepo
from app.exception.subscription_exception import (
    DefaultPlanNotFree,
    NoDefaultPlan,
    OrganizationNotFound,
    PlanNotFound,
    StripeCustomerNotFound,
)
from app.service.stripe_service import StripeService
from stripe import Event, Subscription

logger = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(
        self,
        organization_repo: OrganizationRepo,
        plan_repo: PlanRepo,
        organization_plan_repo: OrganizationPlanRepo,
        stripe_service: StripeService,
    ):
        self.organization_repo = organization_repo
        self.plan_repo = plan_repo
        self.organization_plan_repo = organization_plan_repo
        self.stripe_service = stripe_service

    async def handle_subscription_event(self, event: Event) -> None:
        subscription: Subscription = event.data.object
        details = self.stripe_service.extract_subscription_details(subscription)

        org = await self.organization_repo.get_by_stripe_customer_id(
            details["customer_id"]
        )
        if not org:
            logger.error(
                f"Organization not found for customer_id={details['customer_id']}"
            )
            raise OrganizationNotFound(details["customer_id"])

        plan = await self.plan_repo.get_by_stripe_product_id(details["product_id"])
        if not plan:
            logger.error(f"Plan not found for product_id={details['product_id']}")
            raise PlanNotFound(details["product_id"])

        await self.organization_plan_repo.upsert_plan(
            organization_id=org.id,
            plan_id=plan.id,
            stripe_subscription_id=details["subscription_id"],
            current_period_starts_at=details["period_start"],
            current_period_ends_at=details["period_end"],
            status=details["status"],
        )

        logger.info(
            f"Subscription synced: org_id={org.id}, plan_id={plan.id}, "
            f"sub_id={details['subscription_id']}, status={details['status']}"
        )

    async def handle_subscription_cancelled(self, subscription: Subscription) -> None:
        stripe_subscription_id = subscription.id
        logger.info(f"Handling cancellation of subscription: {stripe_subscription_id}")

        affected = await self.organization_plan_repo.mark_subscription_as_canceled(
            stripe_subscription_id=stripe_subscription_id,
            canceled_at=datetime.fromtimestamp(
                subscription.canceled_at or time.time(), tz=timezone.utc
            ),
            status=subscription.status,
        )

        if affected == 0:
            logger.warning(
                f"No organization_plan found for subscription_id={stripe_subscription_id}"
            )

    async def get_portal_url_for_org(self, org_id: int) -> str:
        customer_id = await self.organization_repo.get_stripe_customer_id(org_id)
        if not customer_id:
            raise StripeCustomerNotFound(org_id)

        return self.stripe_service.create_portal_session(
            customer_id,
            return_url=f"{settings.base_web_url}/dashboard",
        )

    async def provision_free_subscription_if_needed(
        self,
        org_id: int,
        email: str,
        full_name: str,
    ) -> None:
        if await self.organization_plan_repo.has_active_plan(org_id):
            return

        default_plan = await self.plan_repo.get_default_plan()
        if not default_plan:
            raise NoDefaultPlan()

        stripe_customer_id = await self.organization_repo.get_stripe_customer_id(org_id)

        if not stripe_customer_id:
            customer_name = (
                full_name or email
                if settings.mode == "b2c"
                else (await self.organization_repo.get_by_id(org_id)).name
            )
            stripe_customer = self.stripe_service.create_customer(
                email=email,
                name=customer_name,
                metadata={"org_id": org_id},
            )
            stripe_customer_id = stripe_customer.id
            await self.organization_repo.set_stripe_customer_id(
                org_id, stripe_customer_id
            )

        prices = self.stripe_service.list_prices_for_product(
            default_plan.stripe_product_id
        )
        if not prices:
            raise PlanNotFound(stripe_product_id=default_plan.stripe_product_id)

        price = prices[0]
        if price.unit_amount > 0:
            raise DefaultPlanNotFree(plan_id=default_plan.id)

        self.stripe_service.create_free_subscription(stripe_customer_id, price.id)
