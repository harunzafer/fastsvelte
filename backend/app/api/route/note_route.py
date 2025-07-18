from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.model.note_model import CreateNoteRequest, NoteResponse, UpdateNoteRequest
from app.model.role_model import Role
from app.model.user_model import CurrentUser
from app.service.note_service import NoteService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post("/", response_model=NoteResponse)
@inject
async def create_note(
    data: CreateNoteRequest,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = await note_service.create_note(user, data)
    return NoteResponse.model_validate(note.model_dump())


@router.get("/", response_model=list[NoteResponse])
@inject
async def list_notes(
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    notes = await note_service.list_notes(user)
    return [NoteResponse.model_validate(n.model_dump()) for n in notes]


@router.get("/{note_id}", response_model=NoteResponse)
@inject
async def get_note(
    note_id: int,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = await note_service.get_note(user, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return NoteResponse.model_validate(note.model_dump())


@router.put("/{note_id}", response_model=NoteResponse)
@inject
async def update_note(
    note_id: int,
    data: UpdateNoteRequest,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = await note_service.update_note(user, note_id, data)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return NoteResponse.model_validate(note.model_dump())


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_note(
    note_id: int,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    await note_service.delete_note(user, note_id)


@router.post("/{note_id}/summarize", response_model=str)
@inject
async def summarize_note(
    note_id: int,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    summary = await note_service.summarize_note(user, note_id)
    if summary is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return summary
