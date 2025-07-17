from datetime import datetime

from app.data.repo.base_repo import BaseRepo
from app.model.password_model import PasswordResetToken


class PasswordRepo(BaseRepo):
    async def insert_reset_token(
        self, user_id: int, token: str, expires_at: datetime
    ) -> None:
        query = """
            INSERT INTO fastsvelte.password_reset (user_id, token, expires_at)
            VALUES ($1, $2, $3)
        """
        await self.execute(query, user_id, token, expires_at)

    async def get_valid_token(self, token: str) -> PasswordResetToken | None:
        query = """
            SELECT id, user_id, token, created_at, expires_at, used_at, attempts
            FROM fastsvelte.password_reset
            WHERE token = $1 AND used_at IS NULL AND expires_at > now()
        """
        row = await self.fetch_one(query, token)
        return PasswordResetToken(**row) if row else None

    async def mark_token_as_used(self, token: str) -> None:
        query = """
            UPDATE fastsvelte.password_reset
            SET used_at = now()
            WHERE token = $1
        """
        await self.execute(query, token)

    async def update_user_password(self, user_id: int, password_hash: str) -> None:
        query = """
            UPDATE fastsvelte."user"
            SET password_hash = $1, updated_at = now()
            WHERE id = $2 AND deleted_at IS NULL
        """
        await self.execute(query, password_hash, user_id)
