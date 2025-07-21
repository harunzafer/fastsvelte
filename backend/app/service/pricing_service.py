from app.data.repo.pricing_repo import PricingRepo
from app.exception.common_exception import ResourceNotFound
from app.model.pricing_model import (
    CurrentOrgPlanDetail,
    PricingAdminRequest,
    PricingPlan,
    UpdatePricingRequest,
)


class PricingService:
    def __init__(self, pricing_repo: PricingRepo):
        self.pricing_repo = pricing_repo

    async def list_active_plans(self) -> list[PricingPlan]:
        return await self.pricing_repo.list_active_plans()

    async def get_current_plan(self, org_id: int) -> CurrentOrgPlanDetail | None:
        return await self.pricing_repo.get_current_plan(org_id)

    async def assign_plan(self, org_id: int, plan_id: int) -> None:
        plans = await self.pricing_repo.list_active_plans()
        if not any(p.id == plan_id for p in plans):
            raise ResourceNotFound("pricing", plan_id)

        await self.pricing_repo.assign_plan(org_id, plan_id)

    async def list_all_plans(self) -> list[PricingPlan]:
        return await self.pricing_repo.list_all_plans()

    async def create_plan(self, data: PricingAdminRequest) -> int:
        # validate billing_period is one of 'monthly', 'yearly', 'one_time'
        if data.billing_period not in ("monthly", "yearly", "one_time"):
            raise ValueError("Invalid billing period")

        return await self.pricing_repo.create_pricing_plan(data)

    async def update_plan(self, plan_id: int, data: UpdatePricingRequest) -> None:
        await self.pricing_repo.update_pricing_plan(plan_id, data)

    async def soft_delete_plan(self, plan_id: int) -> None:
        await self.pricing_repo.soft_delete_plan(plan_id)

    async def set_default_plan(self, plan_id: int) -> None:
        await self.pricing_repo.set_default_plan(plan_id)
