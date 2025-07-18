from app.data.repo.base_repo import BaseRepo
from app.model.setting_model import OrganizationSettingWithDefinition


class OrganizationSettingRepo(BaseRepo):
    async def get_organization_setting(
        self, organization_id: int, definition_id: int
    ) -> OrganizationSettingWithDefinition | None:
        query = """
            SELECT
                s.id, s.organization_id, s.definition_id, s.value, s.updated_at,
                d.key, d.type, d.description
            FROM fastsvelte.organization_setting s
            JOIN fastsvelte.organization_setting_definition d ON s.definition_id = d.id
            WHERE s.organization_id = $1 AND s.definition_id = $2
        """
        row = await self.fetch_one(query, organization_id, definition_id)
        return OrganizationSettingWithDefinition(**row) if row else None

    async def set_organization_setting(
        self, organization_id: int, definition_id: int, value: str
    ) -> OrganizationSettingWithDefinition:
        upsert_query = """
            INSERT INTO fastsvelte.organization_setting (organization_id, definition_id, value, updated_at)
            VALUES ($1, $2, $3, now())
            ON CONFLICT (organization_id, definition_id) DO UPDATE
            SET value = EXCLUDED.value,
                updated_at = now()
        """
        await self.execute(upsert_query, organization_id, definition_id, value)

        select_query = """
            SELECT
                s.id, s.organization_id, s.definition_id, s.value, s.updated_at,
                d.key, d.type, d.description
            FROM fastsvelte.organization_setting s
            JOIN fastsvelte.organization_setting_definition d ON s.definition_id = d.id
            WHERE s.organization_id = $1 AND s.definition_id = $2
        """
        row = await self.fetch_one(select_query, organization_id, definition_id)
        return OrganizationSettingWithDefinition(**row)

    async def list_organization_settings(
        self, organization_id: int
    ) -> list[OrganizationSettingWithDefinition]:
        query = """
            SELECT
                s.id, s.organization_id, s.definition_id, s.value, s.updated_at,
                d.key, d.type, d.description
            FROM fastsvelte.organization_setting s
            JOIN fastsvelte.organization_setting_definition d ON s.definition_id = d.id
            WHERE s.organization_id = $1
        """
        rows = await self.fetch_all(query, organization_id)
        return [OrganizationSettingWithDefinition(**row) for row in rows]
