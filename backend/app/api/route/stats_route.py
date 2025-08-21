from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.model.role_model import Role
from app.model.user_model import CurrentUser
from app.service.note_service import NoteService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta


class StatsResponse(BaseModel):
    total_notes: int
    recent_notes: int  # last 30 days
    ai_summaries_generated: int  # TODO: track this properly


router = APIRouter()


@router.get("/", response_model=StatsResponse, operation_id="getStats")
@inject
async def get_stats(
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    """Get user statistics for dashboard"""
    notes = await note_service.list_notes(user.id)
    
    # Calculate recent notes (last 30 days)
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    
    recent_count = len([
        note for note in notes 
        if note.updated_at >= thirty_days_ago
    ])
    
    return StatsResponse(
        total_notes=len(notes),
        recent_notes=recent_count,
        ai_summaries_generated=0  # TODO: implement proper tracking
    )