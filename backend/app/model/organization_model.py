from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Organization(BaseModel):
    id: int
    name: str
    stripe_customer_id: Optional[str] = None
    created_at: datetime
    first_seen_at: Optional[datetime] = None
    onboarding_complete_at: Optional[datetime] = None
