from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.exception.auth_exception import AccessDenied
from app.exception.common_exception import ResourceNotFound
from app.model.role_model import Role
from app.model.user_model import CurrentUser, User
from app.service.setting_service import SettingService
from app.service.user_service import UserService
from app.util.permission_util import require_same_org_or_admin
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()


class UpdateSettingRequest(BaseModel):
    key: str
    value: str


@router.get("/user/{user_id}", operation_id="getUserSettings")
@inject
async def get_user_settings(
    user_id: int,
    current_user: CurrentUser = Depends(min_role_required(Role.READONLY)),
    user_service: UserService = Depends(Provide[Container.user_service]),
    setting_service: SettingService = Depends(Provide[Container.setting_service]),
):
    if user_id != current_user.id:
        target_user: User = await user_service.get_user_by_id(user_id)
        if not target_user:
            raise ResourceNotFound("user", user_id)
        require_same_org_or_admin(current_user, target_user, "view settings")

    return await setting_service.list_user_settings(user_id)


@router.post("/user/{user_id}", operation_id="setUserSetting")
@inject
async def set_user_setting(
    user_id: int,
    req: UpdateSettingRequest,
    current_user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    user_service: UserService = Depends(Provide[Container.user_service]),
    setting_service: SettingService = Depends(Provide[Container.setting_service]),
):
    if user_id != current_user.id:
        target_user = await user_service.get_user_by_id(user_id)
        if not target_user:
            raise ResourceNotFound("user", user_id)
        require_same_org_or_admin(current_user, target_user, "update settings")

    return await setting_service.set_user_setting_by_key(user_id, req.key, req.value)


@router.get("/organization/{organization_id}", operation_id="getOrganizationSettings")
@inject
async def get_org_settings(
    organization_id: int,
    current_user: CurrentUser = Depends(min_role_required(Role.ORG_ADMIN)),
    setting_service: SettingService = Depends(Provide[Container.setting_service]),
):
    if (
        current_user.role != Role.SYSTEM_ADMIN
        and organization_id != current_user.organization_id
    ):
        raise AccessDenied("Not authorized to view settings for this organization")

    return await setting_service.list_organization_settings(organization_id)


@router.post("/organization/{organization_id}", operation_id="setOrganizationSetting")
@inject
async def set_org_setting(
    organization_id: int,
    req: UpdateSettingRequest,
    current_user: CurrentUser = Depends(min_role_required(Role.ORG_ADMIN)),
    setting_service: SettingService = Depends(Provide[Container.setting_service]),
):
    if (
        current_user.role != Role.SYSTEM_ADMIN
        and organization_id != current_user.organization_id
    ):
        raise AccessDenied("Not authorized to update settings for this organization")

    return await setting_service.set_organization_setting_by_key(
        organization_id, req.key, req.value
    )
