from typing import Optional

from app.data.repo.base_repo import BaseRepo
from app.model.note_model import Note


class NoteRepo(BaseRepo):
    async def create_note(self, user_id: int, title: str, content: str) -> Note:
        query = """
            INSERT INTO fastsvelte.note (user_id, title, content)
            VALUES ($1, $2, $3)
            RETURNING id, user_id, title, content, created_at, updated_at
        """
        row = await self.fetch_one(query, user_id, title, content)
        return Note(**row)

    async def get_note_by_id(self, note_id: int, user_id: int) -> Optional[Note]:
        query = """
            SELECT id, user_id, title, content, created_at, updated_at
            FROM fastsvelte.note
            WHERE id = $1 AND user_id = $2
        """
        row = await self.fetch_one(query, note_id, user_id)
        return Note(**row) if row else None

    async def list_notes(self, user_id: int) -> list[Note]:
        query = """
            SELECT id, user_id, title, content, created_at, updated_at
            FROM fastsvelte.note
            WHERE user_id = $1
            ORDER BY created_at DESC
        """
        rows = await self.fetch_all(query, user_id)
        return [Note(**row) for row in rows]

    async def update_note(
        self, note_id: int, user_id: int, title: Optional[str], content: Optional[str]
    ) -> Optional[Note]:
        query = """
            UPDATE fastsvelte.note
            SET title = COALESCE($3, title),
                content = COALESCE($4, content),
                updated_at = now()
            WHERE id = $1 AND user_id = $2
            RETURNING id, user_id, title, content, created_at, updated_at
        """
        row = await self.fetch_one(query, note_id, user_id, title, content)
        return Note(**row) if row else None

    async def delete_note(self, note_id: int, user_id: int) -> None:
        query = "DELETE FROM fastsvelte.note WHERE id = $1 AND user_id = $2"
        await self.execute(query, note_id, user_id)
