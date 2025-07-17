from app.api.route.auth_route import router as auth_router
from app.api.route.user_route import router as user_router
from fastapi import FastAPI


def include_all_routers(app: FastAPI):
    app.include_router(user_router, prefix="/users", tags=["Users"])
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
