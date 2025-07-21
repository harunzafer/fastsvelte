from app.data.repo.base_repo import BaseRepo


class OrgRepo(BaseRepo):
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

    async def get_default_pricing_plan_id_tx(self, conn) -> int:
        row = await conn.fetchrow("""
            SELECT id FROM fastsvelte.pricing
            WHERE is_default = TRUE
            LIMIT 1
        """)
        if not row:
            raise Exception("No default pricing plan configured")
        return row["id"]

    async def assign_pricing_plan_tx(self, org_id: int, pricing_id: int, conn) -> None:
        await conn.execute(
            """
            INSERT INTO fastsvelte.organization_pricing (
                organization_id, pricing_id, started_at, is_active
            ) VALUES ($1, $2, now(), TRUE)
        """,
            org_id,
            pricing_id,
        )
