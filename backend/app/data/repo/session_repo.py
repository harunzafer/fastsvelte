import datetime
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

    async def delete_session(self, session_id: str) -> Session | None:
        query = """
        DELETE FROM fastsvelte.session
        WHERE id = $1
        RETURNING id, user_id, expires_at, context
        """
        record = await self.fetch_one(query, session_id)
        return Session(**record) if record else None
