from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.exception.common_exception import ResourceNotFound
from app.model.pricing_model import (
    AssignPricingRequest,
    CurrentOrgPlanDetail,
    PricingAdminRequest,
    PricingPlan,
    UpdatePricingRequest,
)
from app.model.role_model import Role
from app.model.user_model import CurrentUser
from app.service.pricing_service import PricingService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

router = APIRouter()


@router.get("/", response_model=list[PricingPlan], operation_id="listPricingPlans")
@inject
async def list_pricing_plans(
    user: CurrentUser = Depends(min_role_required(Role.READONLY)),
    pricing_service: PricingService = Depends(Provide[Container.pricing_service]),
):
    return await pricing_service.list_active_plans()


@router.get(
    "/current",
    response_model=CurrentOrgPlanDetail,
    operation_id="getCurrentPricingPlan",
)
@inject
async def get_current_pricing(
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    pricing_service: PricingService = Depends(Provide[Container.pricing_service]),
):
    plan = await pricing_service.get_current_plan(user.organization_id)
    if not plan:
        raise ResourceNotFound("pricing", f"organization_id={user.organization_id}")

    return plan


@router.post("/admin/assign", operation_id="adminAssignPricingPlan")
@inject
async def assign_pricing_plan(
    req: AssignPricingRequest,
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    pricing_service: PricingService = Depends(Provide[Container.pricing_service]),
):
    await pricing_service.assign_plan(req.organization_id, req.pricing_id)
    return {"success": True}


@router.get("/admin", response_model=list[PricingPlan], operation_id="adminListPricing")
@inject
async def list_all_pricing_plans(
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    pricing_service: PricingService = Depends(Provide[Container.pricing_service]),
):
    return await pricing_service.list_all_plans()


@router.post("/admin", operation_id="adminCreatePricing")
@inject
async def create_pricing_plan(
    data: PricingAdminRequest,
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    pricing_service: PricingService = Depends(Provide[Container.pricing_service]),
):
    plan_id = await pricing_service.create_plan(data)
    return {"id": plan_id}


@router.put("/admin/{plan_id}", operation_id="adminUpdatePricing")
@inject
async def update_pricing_plan(
    plan_id: int = Path(..., gt=0),
    data: UpdatePricingRequest = ...,
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    pricing_service: PricingService = Depends(Provide[Container.pricing_service]),
):
    await pricing_service.update_plan(plan_id, data)
    return {"success": True}


@router.delete("/admin/{plan_id}", operation_id="adminDeletePricing")
@inject
async def delete_pricing_plan(
    plan_id: int,
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    pricing_service: PricingService = Depends(Provide[Container.pricing_service]),
):
    await pricing_service.soft_delete_plan(plan_id)
    return {"success": True}


@router.post("/admin/{plan_id}/default", operation_id="adminSetDefaultPricing")
@inject
async def set_default_pricing_plan(
    plan_id: int,
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    pricing_service: PricingService = Depends(Provide[Container.pricing_service]),
):
    await pricing_service.set_default_plan(plan_id)
    return {"success": True}
