from datetime import datetime
from typing import Optional

from app.data.repo.base_repo import BaseRepo


class EmailVerificationRepo(BaseRepo):
    async def create_token(
        self, user_id: int, token: str, expires_at: datetime
    ) -> None:
        query = """
            INSERT INTO fastsvelte.email_verification_token (user_id, token, expires_at)
            VALUES ($1, $2, $3)
        """
        await self.execute(query, user_id, token, expires_at)

    async def get_user_id_by_valid_token(self, token: str) -> Optional[int]:
        query = """
            SELECT user_id FROM fastsvelte.email_verification_token
            WHERE token = $1 AND used_at IS NULL AND expires_at > now()
        """
        row = await self.fetch_one(query, token)
        return row["user_id"] if row else None

    async def mark_token_as_used_and_verify_user(self, user_id: int) -> None:
        await self.execute_transaction(
            lambda conn: self._mark_and_verify_tx(conn, user_id)
        )

    async def _mark_and_verify_tx(self, conn, user_id: int) -> None:
        await conn.execute(
            """
            UPDATE fastsvelte."user"
            SET email_verified = TRUE, email_verified_at = now()
            WHERE id = $1
        """,
            user_id,
        )

        await conn.execute(
            """
            UPDATE fastsvelte.email_verification_token
            SET used_at = now()
            WHERE user_id = $1 AND used_at IS NULL
        """,
            user_id,
        )
