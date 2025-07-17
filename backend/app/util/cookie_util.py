from app.config.settings import settings
from fastapi import Request, Response


def get_cookie_value(request: Request, cookie_name: str) -> str | None:
    """Extract a cookie token from the request by cookie name."""
    return request.cookies.get(cookie_name)


def get_token_from_session_cookie(request: Request) -> str | None:
    return get_cookie_value(request, settings.session_cookie_name)


def set_session_cookie(response: Response, token: str) -> None:
    samesite_value = "lax" if settings.environment == "dev" else "strict"
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        httponly=True,
        secure=True,
        samesite=samesite_value,
        max_age=settings.session_cookie_max_age,
        path="/",
    )
