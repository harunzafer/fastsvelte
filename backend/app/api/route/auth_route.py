import asyncio
import logging

from app.api.middleware.auth_handler import get_current_user
from app.config.container import Container
from app.config.settings import settings
from app.exception.auth_exception import (
    EmailNotVerified,
    InvalidCredentials,
)
from app.model.auth_model import (
    LoginRequest,
    LoginSuccess,
    OAuthLoginRequest,  # 👈 new import
    SignupOrgRequest,
    SignupRequest,
    SignupSuccess,
)
from app.model.user_model import (
    CurrentUser,
    User,  # already present
)
from app.service.auth_service import AuthService
from app.service.onboarding_service import OnboardingService
from app.util.cookie_util import clear_session_cookie, set_session_cookie
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status

logger = logging.getLogger(__name__)


router = APIRouter()


@router.post(
    "/signup",
    response_model=SignupSuccess,
    operation_id="signup",
)
@inject
async def signup(
    request: SignupRequest,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    # Service handles all business logic exceptions
    result = await auth_service.signup(request)
    return SignupSuccess(user_id=result.user_id)


@router.post("/signup-org", response_model=SignupSuccess, operation_id="signupOrg")
@inject
async def signup_org(
    request: SignupOrgRequest,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    if settings.mode != "b2b":
        raise HTTPException(status_code=404, detail="Not found")

    result = await auth_service.signup_org(request)
    return SignupSuccess(user_id=result.user_id)


@router.post("/login", response_model=LoginSuccess, operation_id="login")
@inject
async def login(
    request: LoginRequest,
    response: Response,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    onboarding_service: OnboardingService = Depends(
        Provide[Container.onboarding_service]
    ),
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

    # In B2C mode there is a one-to-one relationship between org and user. Each user is ORG_ADMIN of their own organization.
    # For B2B mode, we do onboarding where we create the organization.
    if settings.mode == "b2c":
        try:
            asyncio.create_task(
                onboarding_service.run_first_seen(
                    org_id=user.organization_id,
                    email=user.email,
                    full_name=f"{user.first_name} {user.last_name}",
                )
            )
        except Exception as e:
            # Optional: log and continue
            logger.warning(
                f"Failed to trigger onboarding: org_id={user.organization_id}, error={e}"
            )

    return LoginSuccess(user_id=session.user_id)


@router.post(
    "/oauth/google", response_model=LoginSuccess, operation_id="loginWithGoogle"
)
@inject
async def login_with_google(
    request: OAuthLoginRequest,
    response: Response,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    onboarding_service: OnboardingService = Depends(
        Provide[Container.onboarding_service]
    ),
):
    user: User = await auth_service.login_with_google(request.id_token)

    session, token = await auth_service.create_session(user.id)
    set_session_cookie(response, token)

    if settings.mode == "b2c":
        try:
            asyncio.create_task(
                onboarding_service.run_first_seen(
                    org_id=user.organization_id,
                    email=user.email,
                    full_name=f"{user.first_name} {user.last_name}",
                )
            )
        except Exception as e:
            logger.warning(
                f"Failed to trigger onboarding: org_id={user.organization_id}, error={e}"
            )

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
