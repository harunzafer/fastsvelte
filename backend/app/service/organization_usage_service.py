import logging
from datetime import datetime, timezone

from app.data.repo.organization_plan_repo import OrganizationPlanRepo
from app.data.repo.organization_usage_repo import OrganizationUsageRepo
from app.data.repo.plan_repo import PlanRepo
from app.model.plan_model import FeatureKey
from app.util.quota_util import get_current_quota_period

logger = logging.getLogger(__name__)


class OrganizationUsageService:
    def __init__(
        self,
        usage_repo: OrganizationUsageRepo,
        plan_repo: PlanRepo,
        organization_plan_repo: OrganizationPlanRepo,
    ):
        self.usage_repo = usage_repo
        self.plan_repo = plan_repo
        self.organization_plan_repo = organization_plan_repo

    async def _get_plan_and_period(self, organization_id: int):
        """Get plan and quota period for an organization, falling back to default plan if needed."""
        plan_info = await self.organization_plan_repo.get_current_plan(organization_id)
        
        if plan_info is None:
            # If no plan assigned, use default plan
            plan = await self.plan_repo.get_default_plan()
            if plan is None:
                logger.warning(f"No default plan found for organization {organization_id}")
                return None, None, None
            # Use current time for quota period when no subscription exists
            period_start, period_end = get_current_quota_period(datetime.now(timezone.utc))
        else:
            plan = await self.plan_repo.get_by_id(plan_info.plan_id)
            period_start, period_end = get_current_quota_period(plan_info.subscription_started_at)

        if plan is None:
            logger.warning(f"Plan not found for organization {organization_id}")
            return None, None, None

        return plan, period_start, period_end

    async def check_quota_for(
        self,
        organization_id: int,
        feature_key: FeatureKey,
        amount: int,
    ) -> bool:
        plan, period_start, _ = await self._get_plan_and_period(organization_id)
        if plan is None:
            return False

        usage = await self.usage_repo.get_usage(
            organization_id, feature_key, period_start
        )

        try:
            limit = int(plan.get_feature(feature_key))
        except Exception:
            logger.exception(
                f"Invalid or missing feature '{feature_key}' in plan '{plan.name}' (id={plan.id})"
            )
            raise  # propagate as 500 Internal Server Error

        return (usage + amount) <= limit

    async def update_usage(
        self,
        organization_id: int,
        feature_key: FeatureKey,
        amount: int,
    ) -> None:
        plan, period_start, period_end = await self._get_plan_and_period(organization_id)
        if plan is None:
            return

        try:
            _ = int(plan.get_feature(feature_key))
        except Exception:
            logger.exception(
                f"Invalid or missing feature '{feature_key}' in plan '{plan.name}' (id={plan.id})"
            )
            raise  # propagate as 500 Internal Server Error

        await self.usage_repo.increment_usage(
            organization_id=organization_id,
            feature_key=feature_key,
            period_start=period_start,
            period_end=period_end,
            amount=amount,
        )
