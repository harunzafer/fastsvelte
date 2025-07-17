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
