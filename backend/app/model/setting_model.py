from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SettingType(str, Enum):
    string = "string"
    boolean = "boolean"
    int = "int"
    float = "float"
    json = "json"


class UserSetting(BaseModel):
    id: int
    user_id: int
    definition_id: int
    value: str
    updated_at: datetime


class OrganizationSetting(BaseModel):
    id: int
    organization_id: int
    definition_id: int
    value: str
    updated_at: datetime


class SettingDefinition(BaseModel):
    id: int
    key: str
    type: SettingType
    description: Optional[str]


class UserSettingWithDefinition(UserSetting):
    key: str
    type: SettingType
    description: Optional[str]


class OrganizationSettingWithDefinition(OrganizationSetting):
    key: str
    type: SettingType
    description: Optional[str]


class UpdateSettingRequest(BaseModel):
    key: str
    value: str
