from app.config.container import Container
from app.config.settings import settings
from app.model.auth_model import (
    LoginRequest,
    LoginSuccess,
    SignupRequest,
    SignupSuccess,
)
from app.model.user_model import User
from app.service.auth_service import AuthService
from app.util.cookie_util import set_session_cookie
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

router = APIRouter()

samesite_value = "lax" if settings.environment == "dev" else "strict"


@router.post("/signup", response_model=SignupSuccess, operation_id="signup")
@inject
async def signup(
    request: SignupRequest,
    response: Response,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    signup_session = await auth_service.signup(request)
    set_session_cookie(response, signup_session.token)
    return SignupSuccess(user_id=signup_session.user_id)


@router.post("/login", response_model=LoginSuccess, operation_id="login")
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
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid credentials"},
        )

    session, token = await auth_service.create_session(user.id)
    set_session_cookie(response, token)

    return LoginSuccess(user_id=session.user_id)
