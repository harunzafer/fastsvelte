from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.model.role_model import Role
from app.model.user_model import (
    CurrentUser,
    UpdateAvatarRequest,
    UpdateUserRequest,
    UserResponse,
    UserStatus,
    UserWithRole,
)
from app.service.onboarding_service import OnboardingService
from app.service.user_service import UserService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/me", response_model=UserWithRole, operation_id="getCurrentUser")
async def get_current_user_route(
    user: CurrentUser = Depends(min_role_required(Role.READONLY)),
):
    return UserWithRole.model_validate(user.model_dump())


@router.get("/status", response_model=UserStatus, operation_id="getUserStatus")
@inject
async def get_user_status_route(
    user: CurrentUser = Depends(min_role_required(Role.READONLY)),
    onboarding_service: OnboardingService = Depends(
        Provide[Container.onboarding_service]
    ),
):
    status = await onboarding_service.get_status(user.organization_id)
    return UserStatus(first_seen_status=status)


@router.post("/me/update", operation_id="updateUserInfo")
@inject
async def update_user_info(
    request: UpdateUserRequest,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    await user_service.update_user_info(user.id, request.first_name, request.last_name)
    return {"success": True}


@router.post("/me/avatar", operation_id="updateUserAvatar")
@inject
async def update_user_avatar(
    request: UpdateAvatarRequest,
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    await user_service.update_user_avatar(user.id, request.avatar_data)
    return {"success": True}


@router.get("/", response_model=list[UserResponse], operation_id="listUsers")
@inject
async def list_users(
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    users = await user_service.list_users()
    return [UserResponse.model_validate(u.model_dump()) for u in users]
