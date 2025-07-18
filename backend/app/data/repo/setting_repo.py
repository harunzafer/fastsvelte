from app.data.repo.base_repo import BaseRepo
from app.model.setting_model import SettingDefinition


class SettingRepo(BaseRepo):
    async def get_user_setting_definition(self, key: str) -> SettingDefinition | None:
        query = """
            SELECT id, key, type, description
            FROM fastsvelte.user_setting_definition
            WHERE key = $1
        """
        row = await self.fetch_one(query, key)
        return SettingDefinition(**row) if row else None

    async def get_org_setting_definition(self, key: str) -> SettingDefinition | None:
        query = """
            SELECT id, key, type, description
            FROM fastsvelte.organization_setting_definition
            WHERE key = $1
        """
        row = await self.fetch_one(query, key)
        return SettingDefinition(**row) if row else None
