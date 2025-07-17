from pydantic import BaseModel
from datetime import datetime


class Session(BaseModel):
    id: str  # SHA-256 hash of raw token
    user_id: int
    created_at: datetime
    expires_at: datetime
