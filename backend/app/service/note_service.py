from app.data.repo.note_repo import NoteRepo
from app.model.note_model import CreateNoteRequest, Note, UpdateNoteRequest
from app.service.note_organizer_service import NoteOrganizerService


class NoteService:
    def __init__(self, note_repo: NoteRepo, note_organizer_service: NoteOrganizerService):
        self.note_repo = note_repo
        self.note_organizer_service = note_organizer_service

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

    async def organize_note(self, user_id: int, note_id: int) -> Note | None:
        note = await self.get_note(user_id, note_id)
        if not note:
            return None
        improved_content = await self.note_organizer_service.organize_and_improve(note.content)
        return await self.note_repo.update_note(note_id, user_id, note.title, improved_content)
