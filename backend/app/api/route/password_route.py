from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.model.password_model import (
    ForgotPasswordRequest,
    ResetPasswordDirectRequest,
    ResetPasswordWithTokenRequest,
)
from app.model.role_model import Role
from app.model.user_model import CurrentUser
from app.service.password_service import PasswordService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, BackgroundTasks, Depends

router = APIRouter()


@router.post("/forgot", operation_id="forgotPassword")
@inject
async def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    password_service: PasswordService = Depends(Provide[Container.password_service]),
):
    email, reset_link = await password_service.generate_password_reset_token(
        request.email.strip().lower()
    )
    background_tasks.add_task(
        password_service.email_service.send_password_reset_email,
        email,
        reset_link,
    )
    return {"message": "Reset link sent."}


@router.post("/reset", operation_id="resetPasswordWithToken")
@inject
async def reset_password_with_token(
    request: ResetPasswordWithTokenRequest,
    password_service: PasswordService = Depends(Provide[Container.password_service]),
):
    await password_service.reset_password_with_token(
        token=request.token, new_password=request.new_password
    )
    return {"message": "Password successfully updated."}


@router.post("/update", operation_id="updatePassword")
@inject
async def update_password(
    request: ResetPasswordDirectRequest,
    user: CurrentUser = Depends(min_role_required(Role.READONLY)),
    password_service: PasswordService = Depends(Provide[Container.password_service]),
):
    await password_service.reset_password_direct(user.id, request.new_password)
    return {"message": "Password successfully updated."}
