import secrets
from datetime import datetime, timedelta, timezone

from app.config.settings import settings
from app.data.repo.password_repo import PasswordRepo
from app.data.repo.user_repo import UserRepo
from app.model.password_model import PasswordResetToken
from app.util.auth_util import hash_password


class PasswordService:
    def __init__(self, user_repo: UserRepo, password_repo: PasswordRepo, email_service):
        self.user_repo = user_repo
        self.password_repo = password_repo
        self.email_service = (
            email_service  # assumed to have send_password_reset_email(to, link)
        )

    async def generate_password_reset_token(self, email: str) -> tuple[str, str]:
        user = await self.user_repo.get_user_with_password_by_email(email)
        if not user:
            return email, ""  # do not reveal existence

        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        await self.password_repo.insert_reset_token(user.id, token, expires_at)

        reset_link = f"{settings.base_web_url}/reset-password?token={token}"
        return user.email, reset_link

    async def reset_password_with_token(self, token: str, new_password: str) -> None:
        token_row: PasswordResetToken = await self.password_repo.get_valid_token(token)
        if not token_row:
            raise ValueError("Invalid or expired token")

        hashed = hash_password(new_password)
        await self.password_repo.update_user_password(token_row.user_id, hashed)
        await self.password_repo.mark_token_as_used(token)

    async def reset_password_direct(self, user_id: int, new_password: str) -> None:
        hashed = hash_password(new_password)
        await self.password_repo.update_user_password(user_id, hashed)
