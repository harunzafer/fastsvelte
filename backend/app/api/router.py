from app.api.route.auth_route import router as auth_router
from app.api.route.email_verification_route import router as email_verification_router
from app.api.route.note_route import router as note_router
from app.api.route.password_route import router as password_router
from app.api.route.setting_route import router as setting_router
from app.api.route.user_route import router as user_router
from fastapi import FastAPI


def include_all_routers(app: FastAPI):
    app.include_router(user_router, prefix="/users", tags=["Users"])
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(
        email_verification_router,
        prefix="/auth",
        tags=["Email Verification"],
    )
    app.include_router(
        password_router, prefix="/password", tags=["Password Management"]
    )
    app.include_router(note_router, prefix="/notes", tags=["Notes"])
    app.include_router(setting_router, prefix="/settings", tags=["Settings"])
