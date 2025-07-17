import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import asyncpg
from app.config.settings import settings
from app.data.repo.org_repo import OrgRepo
from app.data.repo.session_repo import SessionRepo
from app.data.repo.user_repo import UserRepo
from app.exception.auth_exception import EmailAlreadyExists, SignupFailed
from app.model.auth_model import SignupRequest, SignupSession
from app.model.session_model import Session
from app.model.user_model import (
    CreateUser,
    CurrentUser,
    User,
    UserWithPassword,
)
from app.util.auth_util import hash_password, verify_password_hash


class AuthService:
    def __init__(
        self, user_repo: UserRepo, session_repo: SessionRepo, org_repo: OrgRepo
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo
        self.org_repo = org_repo

    def generate_session_token(self) -> str:
        return secrets.token_urlsafe(32)  # ~43 chars, secure, URL-safe

    def hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    async def create_session(self, user_id: int) -> tuple[Session, str]:
        token = self.generate_session_token()
        session_id = self.hash_token(token)
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(seconds=settings.session_cookie_max_age)

        session = Session(
            id=session_id, user_id=user_id, created_at=now, expires_at=expires_at
        )
        await self.session_repo.create_session(session)

        # # Audit the login
        # await self.session_audit_service.log_event(
        #     session_id=session_id, user_id=user_id, event="login"
        # )

        return session, token

    async def validate_session_token(self, token: str) -> CurrentUser | None:
        session_id = self.hash_token(token)
        session = await self.session_repo.get_session_by_id(session_id)

        if not session or session.expires_at <= datetime.now(timezone.utc):
            return None

        # Extend session if it's expiring soon
        if session.expires_at <= datetime.now(timezone.utc) + timedelta(
            seconds=settings.session_refresh_threshold
        ):
            session.expires_at = datetime.now(timezone.utc) + timedelta(
                seconds=settings.session_cookie_max_age
            )
            await self.session_repo.update_expiration(session_id, session.expires_at)

        user = await self.user_repo.get_user_with_role_by_id(session.user_id)

        if not user or not user.is_active or user.deleted_at is not None:
            return None

        return CurrentUser(**user.model_dump(), session=session)

    async def signup(self, data: SignupRequest) -> SignupSession:
        # We perform an explicit uniqueness check before creating the user.
        # This avoids consuming an auto-incrementing ID in case of duplicate emails,
        # since PostgreSQL sequences are non-transactional and will increment even if the insert fails.
        #
        # Although this adds an extra query, signups are infrequent, and it's worth the small cost
        # to protect against ID exhaustion from abuse (e.g. signup spam).
        #
        # We still catch UniqueViolationError as a safeguard against race conditions.
        existing = await self.user_repo.get_user_by_email(data.email)
        if existing:
            raise EmailAlreadyExists("Email is already in use")

        password_hash = hash_password(data.password)

        async def tx(conn):
            org_id = await self.org_repo.create_organization_tx(
                f"{data.email}'s Organization", conn
            )

            user = CreateUser(
                email=data.email,
                password_hash=password_hash,
                first_name=data.first_name,
                last_name=data.last_name,
                organization_id=org_id,
            )
            return await self.user_repo.create_user_tx(user, conn)

        try:
            user_id = await self.user_repo.execute_transaction(tx)
        except asyncpg.UniqueViolationError:
            raise EmailAlreadyExists("Email is already in use")  # fallback safeguard
        except Exception as ex:
            raise SignupFailed("Signup failed") from ex

        session, token = await self.create_session(user_id)
        return SignupSession(token=token, user_id=user_id)

    async def verify_credentials(self, email: str, password: str) -> User | None:
        user_with_pw: UserWithPassword = (
            await self.user_repo.get_user_with_password_by_email(email)
        )

        if not user_with_pw:
            return None

        if not verify_password_hash(user_with_pw.password_hash, password):
            return None

        return User(**user_with_pw.model_dump())

    async def invalidate_session(self, session_id: str) -> None:
        await self.session_repo.delete_session(session_id)
        # if session:
        #     await self.session_audit_service.log_event(
        #         session_id=session.id, user_id=session.user_id, event="logout"
        #     )

    async def invalidate_all_sessions(self, user_id: int) -> None:
        await self.session_repo.delete_sessions_by_user_id(user_id)
        # for session in sessions:
        #     await self.session_audit_service.log_event(
        #         session_id=session.id, user_id=user_id, event="logout_all"
        #     )
