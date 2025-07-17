from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class PasswordResetToken(BaseModel):
    id: int
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime
    used_at: datetime | None
    attempts: int


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordWithTokenRequest(BaseModel):
    token: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)


class ResetPasswordDirectRequest(BaseModel):
    new_password: str = Field(..., min_length=8)
