from datetime import datetime
from typing import Optional

from app.model.role_model import Role
from app.model.session_model import Session
from pydantic import BaseModel, EmailStr, Field, model_validator


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None  # ✅ NEW
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


class UserWithRoleAndPlanStatus(UserWithRole):
    needs_plan_selection: bool


class CurrentUser(UserWithRole):
    session: Session


class CreateUser(BaseModel):
    email: EmailStr
    password_hash: Optional[str] = None
    first_name: Optional[str]
    last_name: Optional[str]
    organization_id: int
    role_name: str
    email_verified: Optional[bool] = False
    email_verified_at: Optional[datetime] = None
    avatar_url: Optional[str] = None


class UserWithPassword(User):
    password_hash: str


class OAuthAccount(BaseModel):
    provider_id: str
    provider_user_id: str
    user_id: int
    created_at: datetime


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]


class SystemAdminUserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None
    is_active: bool
    email_verified: bool
    organization_id: int
    role_id: Optional[int]
    created_at: datetime
    updated_at: datetime


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]


class UserStatus(BaseModel):
    first_seen_status: str
    # Future status fields can go here:
    # trial_expires_at: Optional[str] = None
    # subscription_status: Optional[str] = None
    # feature_flags: Optional[dict] = None


class UpdateUserRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @model_validator(mode="after")
    def validate_fields(self) -> "UpdateUserRequest":
        if not self.first_name and not self.last_name:
            raise ValueError(
                "At least one of 'first_name' or 'last_name' must be provided"
            )

        for field_name in ["first_name", "last_name"]:
            value = getattr(self, field_name)
            if value is not None:
                value = value.strip()
                if len(value) < 2:
                    raise ValueError(f"{field_name} must be at least 2 characters long")
                setattr(self, field_name, value)

        return self


class UpdateAvatarRequest(BaseModel):
    avatar_data: str = Field(..., description="Base64 encoded image data with data URL prefix")
    
    @model_validator(mode="after") 
    def validate_avatar(self) -> "UpdateAvatarRequest":
        if not self.avatar_data.startswith('data:image/'):
            raise ValueError("Avatar must be a valid image data URL")
        
        # Extract base64 part and check size
        try:
            header, data = self.avatar_data.split(',', 1)
            import base64
            decoded = base64.b64decode(data)
            
            # 2MB limit
            if len(decoded) > 2 * 1024 * 1024:
                raise ValueError("Avatar image must be smaller than 2MB")
                
            # Check if it's a valid image format
            if not any(fmt in header.lower() for fmt in ['jpeg', 'jpg', 'png', 'webp']):
                raise ValueError("Avatar must be JPEG, PNG, or WebP format")
                
        except Exception as e:
            raise ValueError(f"Invalid image data: {str(e)}")
            
        return self
