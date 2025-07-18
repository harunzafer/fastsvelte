from app.data.repo.base_repo import BaseRepo
from app.model.setting_model import UserSettingWithDefinition


class UserSettingRepo(BaseRepo):
    async def get_user_setting(
        self, user_id: int, definition_id: int
    ) -> UserSettingWithDefinition | None:
        query = """
            SELECT
                s.id, s.user_id, s.definition_id, s.value, s.updated_at,
                d.key, d.type, d.description
            FROM fastsvelte.user_setting s
            JOIN fastsvelte.user_setting_definition d ON s.definition_id = d.id
            WHERE s.user_id = $1 AND s.definition_id = $2
        """
        row = await self.fetch_one(query, user_id, definition_id)
        return UserSettingWithDefinition(**row) if row else None

    async def set_user_setting(
        self, user_id: int, definition_id: int, value: str
    ) -> UserSettingWithDefinition:
        upsert_query = """
            INSERT INTO fastsvelte.user_setting (user_id, definition_id, value, updated_at)
            VALUES ($1, $2, $3, now())
            ON CONFLICT (user_id, definition_id) DO UPDATE
            SET value = EXCLUDED.value,
                updated_at = now()
        """
        await self.execute(upsert_query, user_id, definition_id, value)

        # Then fetch enriched row
        select_query = """
            SELECT
                s.id, s.user_id, s.definition_id, s.value, s.updated_at,
                d.key, d.type, d.description
            FROM fastsvelte.user_setting s
            JOIN fastsvelte.user_setting_definition d ON s.definition_id = d.id
            WHERE s.user_id = $1 AND s.definition_id = $2
        """
        row = await self.fetch_one(select_query, user_id, definition_id)
        return UserSettingWithDefinition(**row)

    async def list_user_settings(self, user_id: int) -> list[UserSettingWithDefinition]:
        query = """
            SELECT
                s.id, s.user_id, s.definition_id, s.value, s.updated_at,
                d.key, d.type, d.description
            FROM fastsvelte.user_setting s
            JOIN fastsvelte.user_setting_definition d ON s.definition_id = d.id
            WHERE s.user_id = $1
        """
        rows = await self.fetch_all(query, user_id)
        return [UserSettingWithDefinition(**row) for row in rows]
