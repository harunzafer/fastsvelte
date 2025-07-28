from datetime import datetime
from enum import Enum
from typing import Literal, Optional, overload

from pydantic import BaseModel


class FeatureKey(str, Enum):
    """
    Each key in this enum must:
    - Match a field in PlanFeatures model
    - Match a key in the plan.features JSON (in DB)

    Update this enum and PlanFeatures together when adding new plan features.
    """

    MAX_NOTES = "max_notes"
    TOKEN_LIMIT = "token_limit"
    ENABLE_AI = "enable_ai"

    def __str__(self) -> str:
        return self.value


class PlanFeatures(BaseModel):
    max_notes: Optional[int]
    token_limit: Optional[int]
    enable_ai: Optional[bool]


class Plan(BaseModel):
    id: int
    name: str
    description: Optional[str]
    features: PlanFeatures
    stripe_product_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    def get_feature(self, key: FeatureKey) -> int | bool | str | None:
        return getattr(self.features, str(key), None)


class CurrentOrgPlanDetail(BaseModel):
    id: int
    organization_id: int
    plan_id: int
    stripe_subscription_id: Optional[str]
    subscription_started_at: datetime
    current_period_starts_at: Optional[datetime]
    current_period_ends_at: Optional[datetime]
    ended_at: Optional[datetime]
    status: Optional[str]

    name: str
    description: Optional[str]
    features: PlanFeatures


class AssignPlanRequest(BaseModel):
    organization_id: int
    plan_id: int


class PlanAdminRequest(BaseModel):
    name: str
    description: Optional[str] = None
    features: dict = {}
    stripe_product_id: Optional[str] = None


class UpdatePlanRequest(BaseModel):
    description: Optional[str] = None
    features: Optional[dict] = None
