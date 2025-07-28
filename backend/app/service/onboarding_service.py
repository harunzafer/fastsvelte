from datetime import datetime, timedelta, timezone

from app.data.repo.organization_plan_repo import OrganizationPlanRepo
from app.data.repo.organization_repo import OrganizationRepo
from app.service.subscription_service import SubscriptionService


class OnboardingService:
    def __init__(
        self,
        organization_repo: OrganizationRepo,
        organization_plan_repo: OrganizationPlanRepo,
        subscription_service: SubscriptionService,
    ):
        self.organization_repo = organization_repo
        self.organization_plan_repo = organization_plan_repo
        self.subscription_service = subscription_service

    async def run_first_seen(self, org_id: int, email: str, full_name: str) -> None:
        """
        Called automatically after first user login (B2C) or manually after org creation (B2B).

        Responsibilities:
        - Set `first_seen_at` if not already set.
        - Ensure Stripe customer exists.
        - Assign the default (free/inactive) plan if none exists.

        This method is intended to bootstrap Stripe state required for billing portal access
        and usage enforcement. It is safe to call multiple times (idempotent).

        Trigger: Immediately after login for B2C users.
        """
        org = await self.organization_repo.get_by_id(org_id)

        if not org.first_seen_at:
            await self.organization_repo.set_first_seen_at(
                org_id, datetime.now(timezone.utc)
            )

        await self.subscription_service.provision_free_subscription_if_needed(
            org_id=org.id,
            email=email,
            full_name=full_name,
        )

    async def run_full_onboarding(self, organization_id: int) -> None:
        """
        Optional hook for product-specific onboarding logic.

        Can be used to:
        - Ask the user for preferences, configuration, workspace setup
        - Send welcome emails or guide tours
        - Trigger integrations or seeding data

        This is not called automatically. It should be triggered by frontend or admin action
        in products where onboarding includes multiple steps after subscription setup.
        """
        await self.organization_repo.set_onboarding_complete_at(
            organization_id, datetime.now(timezone.utc)
        )

    async def get_status(self, org_id: int) -> str:
        org = await self.organization_repo.get_by_id(org_id)
        has_plan = await self.organization_plan_repo.has_active_plan(org_id)

        return compute_first_seen_status(
            first_seen_at=org.first_seen_at,
            stripe_customer_id=org.stripe_customer_id,
            has_active_plan=has_plan,
        )


def compute_first_seen_status(
    first_seen_at: datetime | None,
    stripe_customer_id: str | None,
    has_active_plan: bool,
    max_pending_seconds: int = 20,
) -> str:
    now = datetime.now(timezone.utc)

    if not first_seen_at:
        return "not_started"

    if (not stripe_customer_id or not has_active_plan) and (
        now - first_seen_at > timedelta(seconds=max_pending_seconds)
    ):
        return "error"

    if not stripe_customer_id or not has_active_plan:
        return "in_progress"

    return "complete"
