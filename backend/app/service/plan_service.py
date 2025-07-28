from app.data.repo.plan_repo import PlanRepo
from app.exception.common_exception import ResourceNotFound
from app.model.plan_model import (
    CurrentOrgPlanDetail,
    Plan,
    PlanAdminRequest,
    UpdatePlanRequest,
)


class PlanService:
    def __init__(self, plan_repo: PlanRepo):
        self.plan_repo = plan_repo

    async def list_active_plans(self) -> list[Plan]:
        return await self.plan_repo.list_active_plans()

    async def get_current_plan(self, org_id: int) -> CurrentOrgPlanDetail | None:
        return await self.plan_repo.get_current_plan(org_id)

    async def assign_plan(self, org_id: int, plan_id: int) -> None:
        plans = await self.plan_repo.list_active_plans()
        if not any(p.id == plan_id for p in plans):
            raise ResourceNotFound("plan", plan_id)

        await self.plan_repo.assign_plan(org_id, plan_id)

    async def list_all_plans(self) -> list[Plan]:
        return await self.plan_repo.list_all_plans()

    async def create_plan(self, data: PlanAdminRequest) -> int:
        # validate billing_period is one of 'monthly', 'yearly', 'one_time'
        if data.billing_period not in ("monthly", "yearly", "one_time"):
            raise ValueError("Invalid billing period")

        return await self.plan_repo.create_plan(data)

    async def update_plan(self, plan_id: int, data: UpdatePlanRequest) -> None:
        await self.plan_repo.update_plan(plan_id, data)

    async def soft_delete_plan(self, plan_id: int) -> None:
        await self.plan_repo.soft_delete_plan(plan_id)

    async def set_default_plan(self, plan_id: int) -> None:
        await self.plan_repo.set_default_plan(plan_id)
