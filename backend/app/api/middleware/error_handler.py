from fastapi import Request
from fastapi.responses import JSONResponse
from app.exception.auth_exception import EmailAlreadyExists, SignupFailed


def register_error_handlers(app):
    @app.exception_handler(EmailAlreadyExists)
    async def email_conflict_handler(request: Request, exc: EmailAlreadyExists):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(SignupFailed)
    async def signup_failed_handler(request: Request, exc: SignupFailed):
        return JSONResponse(status_code=500, content={"detail": str(exc)})
