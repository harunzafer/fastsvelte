from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.exception.common_exception import ResourceNotFound
from app.model.plan_model import (
    AssignPlanRequest,
    CurrentOrgPlanDetail,
    Plan,
    PlanAdminRequest,
    UpdatePlanRequest,
)
from app.model.role_model import Role
from app.model.user_model import CurrentUser
from app.service.plan_service import PlanService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

router = APIRouter()


@router.get("/", response_model=list[Plan], operation_id="listPlans")
@inject
async def list_plans(
    user: CurrentUser = Depends(min_role_required(Role.READONLY)),
    plan_service: PlanService = Depends(Provide[Container.plan_service]),
):
    return await plan_service.list_active_plans()


@router.get(
    "/current", response_model=CurrentOrgPlanDetail, operation_id="getCurrentPlan"
)
@inject
async def get_current_plan(
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    plan_service: PlanService = Depends(Provide[Container.plan_service]),
):
    plan = await plan_service.get_current_plan(user.organization_id)
    if not plan:
        raise ResourceNotFound("plan", f"organization_id={user.organization_id}")
    return plan


@router.post("/admin/assign", operation_id="adminAssignPlan")
@inject
async def assign_plan(
    req: AssignPlanRequest,
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    plan_service: PlanService = Depends(Provide[Container.plan_service]),
):
    await plan_service.assign_plan(req.organization_id, req.plan_id)
    return {"success": True}


@router.get("/admin", response_model=list[Plan], operation_id="adminListPlans")
@inject
async def list_all_plans(
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    plan_service: PlanService = Depends(Provide[Container.plan_service]),
):
    return await plan_service.list_all_plans()


@router.post("/admin", operation_id="adminCreatePlan")
@inject
async def create_plan(
    data: PlanAdminRequest,
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    plan_service: PlanService = Depends(Provide[Container.plan_service]),
):
    plan_id = await plan_service.create_plan(data)
    return {"id": plan_id}


@router.put("/admin/{plan_id}", operation_id="adminUpdatePlan")
@inject
async def update_plan(
    plan_id: int = Path(..., gt=0),
    data: UpdatePlanRequest = ...,
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    plan_service: PlanService = Depends(Provide[Container.plan_service]),
):
    await plan_service.update_plan(plan_id, data)
    return {"success": True}


@router.delete("/admin/{plan_id}", operation_id="adminDeletePlan")
@inject
async def delete_plan(
    plan_id: int,
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    plan_service: PlanService = Depends(Provide[Container.plan_service]),
):
    await plan_service.soft_delete_plan(plan_id)
    return {"success": True}


@router.post("/admin/{plan_id}/default", operation_id="adminSetDefaultPlan")
@inject
async def set_default_plan(
    plan_id: int,
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    plan_service: PlanService = Depends(Provide[Container.plan_service]),
):
    await plan_service.set_default_plan(plan_id)
    return {"success": True}
