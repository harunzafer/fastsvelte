from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Invitation(BaseModel):
    id: int
    email: EmailStr
    token: str
    role_name: str
    organization_id: Optional[int] = None
    created_by: Optional[int]
    accepted_at: Optional[datetime]
    expires_at: datetime
    created_at: datetime


class InvitationCreateRequest(BaseModel):
    email: EmailStr
    role: str  # e.g. "admin", "member"


class InvitationAcceptRequest(BaseModel):
    token: str
    password: str
    first_name: str
    last_name: str
    organization_name: Optional[str] = None  # required only if invitation has no org


class InvitationResponse(BaseModel):
    id: int
    email: EmailStr
    role_name: str
    organization_id: Optional[int] = None
    accepted_at: Optional[datetime]
    expires_at: datetime
    created_at: datetime
    created_by: Optional[int]
