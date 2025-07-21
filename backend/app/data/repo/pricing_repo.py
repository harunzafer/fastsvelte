from typing import Optional

from app.data.repo.base_repo import BaseRepo
from app.model.pricing_model import (
    CurrentOrgPlanDetail,
    PricingAdminRequest,
    PricingPlan,
    UpdatePricingRequest,
)


class PricingRepo(BaseRepo):
    async def list_active_plans(self) -> list[PricingPlan]:
        query = """
            SELECT id, name, description, price_cents, billing_period,
                   is_active, metadata, created_at
            FROM fastsvelte.pricing
            WHERE is_active = TRUE
        """
        rows = await self.fetch_all(query)
        return [PricingPlan(**row) for row in rows]

    async def get_current_plan(self, org_id: int) -> Optional[CurrentOrgPlanDetail]:
        query = """
            SELECT 
                op.id, op.organization_id, op.pricing_id, op.started_at, op.expires_at, op.is_active,
                p.name, p.description, p.price_cents, p.billing_period, p.metadata, p.created_at
            FROM fastsvelte.organization_pricing op
            JOIN fastsvelte.pricing p ON op.pricing_id = p.id
            WHERE op.organization_id = $1 AND op.is_active = TRUE
            ORDER BY op.started_at DESC
            LIMIT 1
        """
        row = await self.fetch_one(query, org_id)
        return CurrentOrgPlanDetail(**row) if row else None

    async def assign_plan(self, org_id: int, plan_id: int) -> None:
        async def tx(conn):
            await conn.execute(
                """
                UPDATE fastsvelte.organization_pricing
                SET is_active = FALSE
                WHERE organization_id = $1 AND is_active = TRUE
            """,
                org_id,
            )

            await conn.execute(
                """
                INSERT INTO fastsvelte.organization_pricing (
                    organization_id, pricing_id, started_at, is_active
                ) VALUES ($1, $2, now(), TRUE)
            """,
                org_id,
                plan_id,
            )

        await self.execute_transaction(tx)

    async def list_all_plans(self) -> list[PricingPlan]:
        query = """
            SELECT id, name, description, price_cents, billing_period,
                is_active, is_default, metadata, created_at
            FROM fastsvelte.pricing
            ORDER BY created_at DESC
        """
        rows = await self.fetch_all(query)
        return [PricingPlan(**row) for row in rows]

    async def create_pricing_plan(self, data: PricingAdminRequest) -> int:
        async def tx(conn):
            if data.is_default:
                await conn.execute("""
                    UPDATE fastsvelte.pricing SET is_default = FALSE WHERE is_default = TRUE
                """)
            row = await conn.fetchrow(
                """
                INSERT INTO fastsvelte.pricing (
                    name, description, price_cents, billing_period,
                    is_active, metadata, is_default
                )
                VALUES ($1, $2, $3, $4, TRUE, $5, $6)
                RETURNING id
            """,
                data.name,
                data.description,
                data.price_cents,
                data.billing_period,
                data.metadata,
                data.is_default,
            )
            return row["id"]

        return await self.execute_transaction(tx)

    async def update_pricing_plan(
        self, plan_id: int, data: UpdatePricingRequest
    ) -> None:
        # Dynamic SQL based on provided fields
        updates = []
        args = []
        idx = 1

        for field in [
            "description",
            "price_cents",
            "billing_period",
            "metadata",
            "is_active",
            "is_default",
        ]:
            val = getattr(data, field)
            if val is not None:
                updates.append(f"{field} = ${idx}")
                args.append(val)
                idx += 1

        if not updates:
            return  # nothing to update

        query = f"""
            UPDATE fastsvelte.pricing
            SET {", ".join(updates)}
            WHERE id = ${idx}
        """
        args.append(plan_id)

        async def tx(conn):
            if data.is_default:
                await conn.execute(
                    """
                    UPDATE fastsvelte.pricing
                    SET is_default = FALSE
                    WHERE is_default = TRUE AND id <> $1
                """,
                    plan_id,
                )
            await conn.execute(query, *args)

        await self.execute_transaction(tx)

    async def soft_delete_plan(self, plan_id: int) -> None:
        query = """
            UPDATE fastsvelte.pricing
            SET is_active = FALSE, is_default = FALSE
            WHERE id = $1
        """
        await self.execute(query, plan_id)

    async def set_default_plan(self, plan_id: int) -> None:
        async def tx(conn):
            await conn.execute(
                """
                UPDATE fastsvelte.pricing
                SET is_default = FALSE
                WHERE is_default = TRUE AND id <> $1
            """,
                plan_id,
            )

            await conn.execute(
                """
                UPDATE fastsvelte.pricing
                SET is_default = TRUE
                WHERE id = $1
            """,
                plan_id,
            )

        await self.execute_transaction(tx)
