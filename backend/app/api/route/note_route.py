from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.exception.common_exception import ResourceNotFound
from app.model.note_model import CreateNoteRequest, NoteResponse, UpdateNoteRequest
from app.model.role_model import Role
from app.model.user_model import CurrentUser
from app.service.note_service import NoteService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/", response_model=NoteResponse, operation_id="createNote")
@inject
async def create_note(
    data: CreateNoteRequest,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = await note_service.create_note(user.id, data)
    return NoteResponse.model_validate(note.model_dump())


@router.get("/", response_model=list[NoteResponse], operation_id="listNotes")
@inject
async def list_notes(
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    notes = await note_service.list_notes(user.id)
    return [NoteResponse.model_validate(n.model_dump()) for n in notes]


@router.get("/{note_id}", response_model=NoteResponse, operation_id="getNote")
@inject
async def get_note(
    note_id: int,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = await note_service.get_note(user.id, note_id)
    if not note:
        raise ResourceNotFound("note", note_id)
    return NoteResponse.model_validate(note.model_dump())


@router.put("/{note_id}", response_model=NoteResponse, operation_id="updateNote")
@inject
async def update_note(
    note_id: int,
    data: UpdateNoteRequest,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = await note_service.update_note(user.id, note_id, data)
    if not note:
        raise ResourceNotFound("note", note_id)
    return NoteResponse.model_validate(note.model_dump())


@router.delete("/{note_id}", status_code=204, operation_id="deleteNote")
@inject
async def delete_note(
    note_id: int,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = await note_service.get_note(user.id, note_id)
    if not note:
        raise ResourceNotFound("note", note_id)
    await note_service.delete_note(user.id, note_id)


@router.post("/{note_id}/summarize", response_model=str, operation_id="summarizeNote")
@inject
async def summarize_note(
    note_id: int,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    summary = await note_service.summarize_note(user.id, note_id)
    if summary is None:
        raise ResourceNotFound("note", note_id)
    return summary
