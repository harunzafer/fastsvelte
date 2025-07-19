from app.config.container import Container
from app.exception.auth_exception import (
    EmailAlreadyVerified,
    InvalidVerificationToken,
)
from app.exception.common_exception import ResourceNotFound
from app.model.auth_model import ResendVerificationRequest
from app.service.email_verification_service import EmailVerificationService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

router = APIRouter()


@router.post("/verify-email", operation_id="verifyEmail")
@inject
async def verify_email(
    token: str = Query(...),
    service: EmailVerificationService = Depends(Provide[Container.email_verification_service]),
):
    verified = await service.verify_email(token)
    if not verified:
        raise InvalidVerificationToken()
    return {"success": True}


@router.post("/resend-verification", operation_id="resendVerificationEmail")
@inject
async def resend_verification(
    request: ResendVerificationRequest,
    service: EmailVerificationService = Depends(Provide[Container.email_verification_service]),
):
    user = await service.get_user_by_email(request.email)
    if not user:
        raise ResourceNotFound("user", request.email)

    if user.email_verified:
        raise EmailAlreadyVerified()

    await service.send_verification_email(user.id, user.email)
    return {"success": True}
