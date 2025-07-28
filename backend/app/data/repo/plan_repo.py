from typing import Optional

from app.data.repo.base_repo import BaseRepo
from app.model.plan_model import (
    CurrentOrgPlanDetail,
    Plan,
    PlanAdminRequest,
    UpdatePlanRequest,
)


class PlanRepo(BaseRepo):
    async def list_active_plans(self) -> list[Plan]:
        query = """
            SELECT id, name, description, features, stripe_product_id,
                   created_at, updated_at
            FROM fastsvelte.plan
            WHERE is_active = TRUE
        """
        rows = await self.fetch_all(query)
        return [Plan(**row) for row in rows]

    async def list_all_plans(self) -> list[Plan]:
        query = """
            SELECT id, name, description, features, stripe_product_id,
                   created_at, updated_at
            FROM fastsvelte.plan
            ORDER BY created_at DESC
        """
        rows = await self.fetch_all(query)
        return [Plan(**row) for row in rows]

    async def get_by_stripe_product_id(self, product_id: str) -> Optional[Plan]:
        query = """
            SELECT id, name, description, features, stripe_product_id,
                   created_at, updated_at
            FROM fastsvelte.plan
            WHERE stripe_product_id = $1
        """
        row = await self.fetch_one(query, product_id)
        return Plan(**row) if row else None

    async def get_current_plan(self, org_id: int) -> Optional[CurrentOrgPlanDetail]:
        query = """
            SELECT 
                op.id, op.organization_id, op.plan_id,
                op.stripe_subscription_id, op.subscription_started_at,
                op.current_period_starts_at, op.current_period_ends_at,
                op.ended_at, op.status,
                p.name, p.description, p.features
            FROM fastsvelte.organization_plan op
            JOIN fastsvelte.plan p ON op.plan_id = p.id
            WHERE op.organization_id = $1
            ORDER BY op.subscription_started_at DESC
            LIMIT 1
        """
        row = await self.fetch_one(query, org_id)
        return CurrentOrgPlanDetail(**row) if row else None

    async def create_plan(self, data: PlanAdminRequest) -> int:
        query = """
            INSERT INTO fastsvelte.plan (
                name, description, features, stripe_product_id
            )
            VALUES ($1, $2, $3, $4)
            RETURNING id
        """
        row = await self.fetch_one(
            query,
            data.name,
            data.description,
            data.features,
            data.stripe_product_id,
        )
        return row["id"]

    async def update_plan(self, plan_id: int, data: UpdatePlanRequest) -> None:
        updates = []
        args = []
        idx = 1

        for field in ["description", "features"]:
            val = getattr(data, field)
            if val is not None:
                updates.append(f"{field} = ${idx}")
                args.append(val)
                idx += 1

        if not updates:
            return

        query = f"""
            UPDATE fastsvelte.plan
            SET {", ".join(updates)}, updated_at = now()
            WHERE id = ${idx}
        """
        args.append(plan_id)
        await self.execute(query, *args)

    async def soft_delete_plan(self, plan_id: int) -> None:
        query = """
            UPDATE fastsvelte.plan
            SET is_active = FALSE, updated_at = now()
            WHERE id = $1
        """
        await self.execute(query, plan_id)

    async def get_by_id(self, plan_id: int) -> Plan | None:
        query = """
            SELECT id, name, description, features, stripe_product_id,
                   created_at, updated_at
            FROM fastsvelte.plan
            WHERE id = $1
        """
        row = await self.fetch_one(query, plan_id)
        return Plan(**row) if row else None

    async def get_default_plan(self) -> Plan | None:
        query = """
            SELECT id, name, description, features, stripe_product_id,
                   created_at, updated_at
            FROM fastsvelte.plan
            WHERE is_default = TRUE
            LIMIT 1
        """
        row = await self.fetch_one(query)
        return Plan(**row) if row else None
