from datetime import datetime
from typing import Optional

from app.data.repo.base_repo import BaseRepo


class OrganizationUsageRepo(BaseRepo):
    async def get_usage(
        self, organization_id: int, feature_key: str, period_start: datetime
    ) -> int:
        row = await self.fetch_one(
            """
            SELECT usage_count
            FROM fastsvelte.org_usage
            WHERE organization_id = $1 AND feature_key = $2 AND period_start = $3
            """,
            organization_id,
            feature_key,
            period_start,
        )
        return row["usage_count"] if row else 0

    async def increment_usage(
        self,
        organization_id: int,
        feature_key: str,
        period_start: datetime,
        period_end: datetime,
        amount: int,
    ) -> None:
        await self.execute(
            """
            INSERT INTO fastsvelte.org_usage (
                organization_id, feature_key, usage_count, period_start, period_end
            )
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (organization_id, feature_key, period_start)
            DO UPDATE SET usage_count = GREATEST(org_usage.usage_count + EXCLUDED.usage_count, 0)
            """,
            organization_id,
            feature_key,
            amount,
            period_start,
            period_end,
        )
