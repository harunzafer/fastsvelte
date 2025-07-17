from datetime import datetime
from typing import Optional

from app.model.role_model import Role
from app.model.session_model import Session
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    email_verified: bool = False
    email_verified_at: Optional[datetime] = None
    is_active: bool = False
    deleted_at: Optional[datetime] = None
    organization_id: int
    role_id: Optional[int]
    created_at: datetime
    updated_at: datetime


class UserWithRole(User):
    role: Role


class CurrentUser(UserWithRole):
    session: Session


class CreateUser(BaseModel):
    email: EmailStr
    password_hash: str
    first_name: Optional[str]
    last_name: Optional[str]
    organization_id: int


class UserWithPassword(User):
    password_hash: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]


class UpdateUserRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]


# should we keep this here or move to a separate file?
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
