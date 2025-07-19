import secrets
from datetime import datetime, timedelta, timezone

from app.config.settings import settings
from app.data.repo.email_verification_repo import EmailVerificationRepo
from app.data.repo.user_repo import UserRepo
from app.service.email_service_base import EmailService


class EmailVerificationService:
    def __init__(
        self,
        email_service: EmailService,
        email_verification_repo: EmailVerificationRepo,
        user_repo: UserRepo,
    ):
        self.email_service = email_service
        self.email_verification_repo = email_verification_repo
        self.user_repo = user_repo
        self.frontend_url = settings.base_web_url.rstrip("/")

    async def send_verification_email(self, user_id: int, email: str) -> None:
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

        await self.email_verification_repo.create_token(user_id, token, expires_at)

        link = f"{self.frontend_url}/verify-email?token={token}"
        await self.email_service.send_email_verification(
            email=email, verification_link=link
        )

    async def verify_email(self, token: str) -> bool:
        user_id = await self.email_verification_repo.get_user_id_by_valid_token(token)
        if not user_id:
            return False

        await self.email_verification_repo.mark_token_as_used_and_verify_user(user_id)
        return True

    async def get_user_by_email(self, email: str):
        return await self.user_repo.get_user_by_email(email)
