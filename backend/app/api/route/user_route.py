from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.model.role_model import Role
from app.model.user_model import CurrentUser, UserResponse, UserWithRole
from app.service.user_service import UserService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/me", response_model=UserWithRole, operation_id="getCurrentUser")
async def get_current_user_route(
    user: CurrentUser = Depends(min_role_required(Role.READONLY)),
):
    return UserWithRole.model_validate(user.model_dump())


@router.get("/", response_model=list[UserResponse], operation_id="listUsers")
@inject
async def list_users(
    user: CurrentUser = Depends(min_role_required(Role.SYSTEM_ADMIN)),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    users = await user_service.list_users()
    return [UserResponse.model_validate(u.model_dump()) for u in users]
