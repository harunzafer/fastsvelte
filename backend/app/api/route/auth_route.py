from app.api.middleware.auth_handler import get_current_user
from app.config.container import Container
from app.exception.auth_exception import (
    EmailNotVerified,
    InvalidCredentials,
)
from app.model.auth_model import (
    LoginRequest,
    LoginSuccess,
    SignupRequest,
    SignupSuccess,
)
from app.model.user_model import CurrentUser, User
from app.service.auth_service import AuthService
from app.util.cookie_util import clear_session_cookie, set_session_cookie
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

router = APIRouter()

@router.post(
    "/signup",
    response_model=SignupSuccess,
    operation_id="signup",
)
@inject
async def signup(
    request: SignupRequest,
    response: Response,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    # Service handles all business logic exceptions
    result = await auth_service.signup(request)
    return SignupSuccess(user_id=result.user_id)


@router.post(
    "/login",
    response_model=LoginSuccess,
    operation_id="login",
)
@inject
async def login(
    request: LoginRequest,
    response: Response,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    user: User = await auth_service.verify_credentials(
        request.email.strip().lower(), request.password
    )

    if not user:
        raise InvalidCredentials()

    if not user.email_verified:
        raise EmailNotVerified()

    session, token = await auth_service.create_session(user.id)
    set_session_cookie(response, token)

    return LoginSuccess(user_id=session.user_id)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="logout",
)
@inject
async def logout(
    response: Response,
    user: CurrentUser = Depends(get_current_user),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    await auth_service.invalidate_session(user.session.id)
    clear_session_cookie(response)