from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class PricingPlan(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price_cents: int
    billing_period: str  # 'one_time', 'monthly', 'yearly'
    is_active: bool
    is_default: bool
    metadata: dict
    created_at: datetime


class CurrentOrgPlanDetail(BaseModel):
    id: int
    organization_id: int
    pricing_id: int
    started_at: datetime
    expires_at: Optional[datetime]
    is_active: bool

    name: str
    description: Optional[str]
    price_cents: int
    billing_period: str
    metadata: dict
    created_at: datetime  # from pricing table


class AssignPricingRequest(BaseModel):
    organization_id: int
    pricing_id: int


class PricingAdminRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price_cents: int
    billing_period: Literal["monthly", "yearly", "one_time"]
    metadata: dict
    is_default: bool = False


class UpdatePricingRequest(BaseModel):
    description: Optional[str] = None
    price_cents: Optional[int] = None
    billing_period: Optional[Literal["monthly", "yearly", "one_time"]] = None
    metadata: Optional[dict] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
