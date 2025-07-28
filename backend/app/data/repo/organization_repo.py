from datetime import datetime

from app.data.repo.base_repo import BaseRepo
from app.model.organization_model import Organization


class OrganizationRepo(BaseRepo):
    async def create_organization(self, name: str) -> int:
        query = self._create_organization_query()
        row = await self.fetch_one(query, name)
        return row["id"]

    async def create_organization_tx(self, name: str, conn) -> int:
        query = self._create_organization_query()
        row = await conn.fetchrow(query, name)
        return row["id"]

    def _create_organization_query(self) -> str:
        return """
            INSERT INTO fastsvelte.organization (name)
            VALUES ($1)
            RETURNING id
        """

    async def get_by_id(self, org_id: int) -> Organization:
        query = """
            SELECT id, name, stripe_customer_id, created_at, first_seen_at, onboarding_complete_at
            FROM fastsvelte.organization
            WHERE id = $1
        """
        row = await self.fetch_one(query, org_id)
        return Organization(**row)

    async def get_by_stripe_customer_id(
        self, stripe_customer_id: str
    ) -> Organization | None:
        query = """
            SELECT id, name, stripe_customer_id, created_at, first_seen_at, onboarding_complete_at
            FROM fastsvelte.organization
            WHERE stripe_customer_id = $1
        """
        row = await self.fetch_one(query, stripe_customer_id)
        return Organization(**row) if row else None

    async def set_stripe_customer_id(
        self, org_id: int, stripe_customer_id: str
    ) -> None:
        query = """
            UPDATE fastsvelte.organization
            SET stripe_customer_id = $2
            WHERE id = $1
        """
        await self.execute(query, org_id, stripe_customer_id)

    async def get_stripe_customer_id(self, organization_id: int) -> str | None:
        query = """
            SELECT stripe_customer_id
            FROM fastsvelte.organization
            WHERE id = $1
        """
        row = await self.fetch_one(query, organization_id)
        return row["stripe_customer_id"] if row else None

    async def set_first_seen_at(self, org_id: int, ts: datetime) -> None:
        query = """
            UPDATE fastsvelte.organization
            SET first_seen_at = $2
            WHERE id = $1 AND first_seen_at IS NULL
        """
        await self.execute(query, org_id, ts)

    async def set_onboarding_complete_at(self, org_id: int, ts: datetime) -> None:
        query = """
            UPDATE fastsvelte.organization
            SET onboarding_complete_at = $2
            WHERE id = $1 AND onboarding_complete_at IS NULL
        """
        await self.execute(query, org_id, ts)
