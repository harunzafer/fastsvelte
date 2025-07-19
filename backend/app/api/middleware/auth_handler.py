from app.config.container import Container
from app.config.settings import settings
from app.exception.auth_exception import AccessDenied, Unauthorized
from app.model.role_model import Role
from app.model.user_model import CurrentUser, UserWithRole
from app.service.auth_service import AuthService
from app.util.cookie_util import get_cookie_value
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request


@inject
async def get_current_user(
    request: Request,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> UserWithRole:
    token = get_cookie_value(request, settings.session_cookie_name)
    if not token:
        raise Unauthorized("Missing session token")

    user: CurrentUser = await auth_service.validate_session_token(token)

    if not user:
        raise Unauthorized("Invalid or expired session token")

    return user


def min_role_required(min_role: Role):
    async def role_guard(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if user.role < min_role:
            raise AccessDenied()
        return user

    return role_guard
