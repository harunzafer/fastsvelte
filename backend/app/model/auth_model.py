from typing import Optional

from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]


class SignupOrgRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    organization_name: str


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


class OAuthLoginRequest(BaseModel):
    code: str
    state: Optional[str] = None


class OAuthAuthorizationResponse(BaseModel):
    authorization_url: str
