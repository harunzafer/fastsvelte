from app.data.repo.note_repo import NoteRepo
from app.model.note_model import CreateNoteRequest, Note, UpdateNoteRequest
from app.service.summary_service import SummaryService


class NoteService:
    def __init__(self, note_repo: NoteRepo, summary_service: SummaryService):
        self.note_repo = note_repo
        self.summary_service = summary_service

    async def create_note(self, user_id: int, data: CreateNoteRequest) -> Note:
        return await self.note_repo.create_note(user_id, data.title, data.content)

    async def list_notes(self, user_id: int) -> list[Note]:
        return await self.note_repo.list_notes(user_id)

    async def get_note(self, user_id: int, note_id: int) -> Note | None:
        return await self.note_repo.get_note_by_id(note_id, user_id)

    async def update_note(
        self, user_id: int, note_id: int, data: UpdateNoteRequest
    ) -> Note | None:
        return await self.note_repo.update_note(
            note_id, user_id, data.title, data.content
        )

    async def delete_note(self, user_id: int, note_id: int) -> None:
        await self.note_repo.delete_note(note_id, user_id)

    async def summarize_note(self, user_id: int, note_id: int) -> str | None:
        note = await self.get_note(user_id, note_id)
        if not note:
            return None
        return await self.summary_service.summarize(note.content)
