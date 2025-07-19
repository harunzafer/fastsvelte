from typing import Optional

from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]


class SignupSuccess(BaseModel):
    user_id: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginSuccess(BaseModel):
    user_id: int


class SignupResult(BaseModel):
    user_id: int


class ResendVerificationRequest(BaseModel):
    email: EmailStr
