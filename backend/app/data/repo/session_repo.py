from datetime import datetime, timedelta, timezone

from app.data.repo.base_repo import BaseRepo
from app.model.session_model import Session


class SessionRepo(BaseRepo):
    async def create_session(self, session: Session) -> None:
        query = """
            INSERT INTO fastsvelte.session (id, user_id, expires_at, created_at)
            VALUES ($1, $2, $3, $4)
        """
        await self.execute(
            query, session.id, session.user_id, session.expires_at, session.created_at
        )

    async def get_session_by_id(self, session_id: str) -> Session | None:
        query = """
            SELECT id, user_id, created_at, expires_at
            FROM fastsvelte.session
            WHERE id = $1
        """
        row = await self.fetch_one(query, session_id)
        return Session(**row) if row else None

    async def update_expiration(
        self, session_id: str, new_expiration: datetime
    ) -> None:
        query = """
        UPDATE fastsvelte.session
        SET expires_at = $1
        WHERE id = $2
        """
        await self.execute(query, new_expiration, session_id)

    async def delete_session(self, session_id: str) -> None:
        query = """
        DELETE FROM fastsvelte.session
        WHERE id = $1        
        """
        await self.execute(query, session_id)

    async def delete_sessions_by_user_id(self, user_id: int) -> None:
        query = """
        DELETE FROM fastsvelte.session
        WHERE user_id = $1
        """
        await self.execute(query, user_id)

    async def delete_expired_older_than(self, days: int) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        query = """
            DELETE FROM fastsvelte.session
            WHERE expires_at < $1 AND created_at < $1
            RETURNING id
        """
        rows = await self.fetch_all(query, cutoff)
        return len(rows)
