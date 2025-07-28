from datetime import datetime

from app.data.repo.base_repo import BaseRepo
from app.model.plan_model import CurrentOrgPlanDetail


class OrganizationPlanRepo(BaseRepo):
    async def upsert_plan(
        self,
        organization_id: int,
        plan_id: int,
        stripe_subscription_id: str,
        current_period_starts_at: datetime,
        current_period_ends_at: datetime,
        status: str,
    ) -> None:
        query = """
            INSERT INTO fastsvelte.organization_plan (
                organization_id,
                plan_id,
                stripe_subscription_id,
                subscription_started_at,
                current_period_starts_at,
                current_period_ends_at,
                status,
                created_at,
                updated_at
            )
            VALUES ($1, $2, $3, now(), $4, $5, $6, now(), now())
            ON CONFLICT (stripe_subscription_id) DO UPDATE SET
                plan_id = EXCLUDED.plan_id,
                current_period_starts_at = EXCLUDED.current_period_starts_at,
                current_period_ends_at = EXCLUDED.current_period_ends_at,
                status = EXCLUDED.status,
                updated_at = now()
        """
        await self.execute(
            query,
            organization_id,
            plan_id,
            stripe_subscription_id,
            current_period_starts_at,
            current_period_ends_at,
            status,
        )

    async def get_current_plan(
        self, organization_id: int
    ) -> CurrentOrgPlanDetail | None:
        query = """
            SELECT
                op.id,
                op.organization_id,
                op.plan_id,
                op.stripe_subscription_id,
                op.subscription_started_at,
                op.current_period_starts_at,
                op.current_period_ends_at,
                op.ended_at,
                op.status,
                op.created_at,
                op.updated_at,
                p.name,
                p.description,
                p.features
            FROM fastsvelte.organization_plan op
            JOIN fastsvelte.plan p ON p.id = op.plan_id
            WHERE op.organization_id = $1
            ORDER BY op.subscription_started_at DESC
            LIMIT 1
        """
        row = await self.fetch_one(query, organization_id)
        return CurrentOrgPlanDetail(**row) if row else None

    async def has_active_plan(self, org_id: int) -> bool:
        query = """
            SELECT EXISTS (
                SELECT 1
                FROM fastsvelte.organization_plan
                WHERE organization_id = $1
                AND ended_at IS NULL
                AND status IN ('active', 'trialing', 'past_due', 'unpaid')  -- Stripe-valid statuses
            )
        """
        row = await self.fetch_one(query, org_id)
        return row["exists"]

    async def mark_subscription_as_canceled(
        self,
        stripe_subscription_id: str,
        canceled_at: datetime,
        status: str,
    ) -> None:
        query = """
            UPDATE fastsvelte.organization_plan
            SET status = $1,
                ended_at = $2,
                updated_at = now()
            WHERE stripe_subscription_id = $3
        """
        await self.execute(query, status, canceled_at, stripe_subscription_id)
