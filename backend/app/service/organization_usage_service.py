import logging

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

    async def check_quota_for(
        self,
        organization_id: int,
        feature_key: FeatureKey,
        amount: int,
    ) -> bool:
        plan_info = await self.organization_plan_repo.get_current_plan(organization_id)
        plan = await self.plan_repo.get_by_id(plan_info.plan_id)

        period_start, _ = get_current_quota_period(plan_info.subscription_started_at)
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
        plan_info = await self.organization_plan_repo.get_current_plan(organization_id)
        plan = await self.plan_repo.get_by_id(plan_info.plan_id)

        try:
            _ = int(plan.get_feature(feature_key))
        except Exception:
            logger.exception(
                f"Invalid or missing feature '{feature_key}' in plan '{plan.name}' (id={plan.id})"
            )
            raise  # propagate as 500 Internal Server Error

        period_start, period_end = get_current_quota_period(
            plan_info.subscription_started_at
        )

        await self.usage_repo.increment_usage(
            organization_id=organization_id,
            feature_key=feature_key,
            period_start=period_start,
            period_end=period_end,
            amount=amount,
        )
