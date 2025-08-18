import asyncio
import logging
from urllib.parse import urlencode

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
    OAuthAuthorizationResponse,
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
from app.util.oauth_util import (
    OAuthStateError,
    generate_oauth_state,
    map_oauth_error,
    validate_oauth_state,
)
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse

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


@router.get(
    "/oauth/google/authorize-url",
    response_model=OAuthAuthorizationResponse,
    operation_id="getGoogleAuthUrl",
)
async def get_google_auth_url():
    redirect_url = f"{settings.base_api_url}/auth/oauth/google/callback"

    # Generate secure state parameter for CSRF protection
    state = generate_oauth_state()

    # Create authorization URL using direct Google OAuth2 approach
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": redirect_url,
        "scope": "https://www.googleapis.com/auth/userinfo.profile openid email",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }

    authorization_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    )

    return OAuthAuthorizationResponse(authorization_url=authorization_url)


@router.get("/oauth/google/callback", operation_id="googleOAuthCallback")
@inject
async def google_oauth_callback(
    code: str = None,
    state: str = None,
    error: str = None,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    onboarding_service: OnboardingService = Depends(
        Provide[Container.onboarding_service]
    ),
):
    # Handle OAuth errors (user cancelled, access denied, etc.)
    if error:
        logger.info(f"OAuth error: {error}")
        error_code = map_oauth_error(error)
        return RedirectResponse(
            url=f"{settings.base_web_url}/login?error={error_code}", status_code=302
        )

    # Validate required code parameter
    if not code:
        logger.warning("OAuth callback missing authorization code")
        return RedirectResponse(
            url=f"{settings.base_web_url}/login?error=oauth_missing_code",
            status_code=302,
        )

    # Validate state parameter for CSRF protection
    try:
        validate_oauth_state(state)
    except OAuthStateError as e:
        logger.warning(f"OAuth state validation failed: {e}")
        return RedirectResponse(
            url=f"{settings.base_web_url}/login?error=oauth_invalid_state",
            status_code=302,
        )

    try:
        user: User = await auth_service.login_with_google(code)

        # Create session token for cookie
        session, token = await auth_service.create_session(user.id)

        # Create redirect response to frontend dashboard
        redirect_response = RedirectResponse(
            url=f"{settings.base_web_url}", status_code=302
        )

        # Set session cookie
        set_session_cookie(redirect_response, token)

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

        return redirect_response

    except Exception as e:
        logger.error(f"OAuth callback failed: {e}")
        # Redirect to login with error
        return RedirectResponse(
            url=f"{settings.base_web_url}/login?error=oauth_failed", status_code=302
        )


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
