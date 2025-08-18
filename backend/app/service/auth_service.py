import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone

import asyncpg
from app.config.settings import settings
from app.data.repo.organization_repo import OrganizationRepo
from app.data.repo.session_repo import SessionRepo
from app.data.repo.user_repo import UserRepo
from app.exception.auth_exception import EmailAlreadyExists, SignupFailed
from app.model.auth_model import SignupOrgRequest, SignupRequest, SignupResult
from app.model.role_model import Role
from app.model.session_model import Session
from app.model.user_model import (
    CreateUser,
    CurrentUser,
    User,
    UserWithPassword,
)
from app.service.email_verification_service import EmailVerificationService
from app.util.hash_util import hash_password, verify_password_hash

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(
        self,
        user_repo: UserRepo,
        session_repo: SessionRepo,
        org_repo: OrganizationRepo,
        email_verification_service: EmailVerificationService,
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo
        self.org_repo = org_repo
        self.email_verification_service = email_verification_service

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

    async def signup(self, data: SignupRequest) -> SignupResult:
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
            raise EmailAlreadyExists()

        password_hash = hash_password(data.password)

        async def tx(conn):
            org_id = await self.org_repo.create_organization_tx(
                f"{data.email}'s Organization", conn
            )

            # In b2c mode, each customer has one and only one organization
            role_name = (
                Role.ORG_ADMIN.name if settings.mode == "b2c" else Role.MEMBER.name
            )

            user = CreateUser(
                email=data.email,
                password_hash=password_hash,
                first_name=data.first_name,
                last_name=data.last_name,
                organization_id=org_id,
                role_name=role_name,
            )
            user_id = await self.user_repo.create_user_tx(user, conn)
            return user_id, org_id

        try:
            user_id, org_id = await self.user_repo.execute_transaction(tx)
        except asyncpg.UniqueViolationError:
            raise EmailAlreadyExists()  # fallback safeguard
        except Exception as ex:
            logger.error(ex)
            raise SignupFailed()

        # Send verification email
        await self.email_verification_service.send_verification_email(
            user_id=user_id, email=data.email
        )

        return SignupResult(user_id=user_id)

    async def signup_org(self, data: SignupOrgRequest) -> SignupResult:
        existing = await self.user_repo.get_user_by_email(data.email)
        if existing:
            raise EmailAlreadyExists()

        password_hash = hash_password(data.password)

        async def tx(conn):
            org_id = await self.org_repo.create_organization_tx(
                data.organization_name, conn
            )

            user = CreateUser(
                email=data.email,
                password_hash=password_hash,
                first_name=data.first_name,
                last_name=data.last_name,
                organization_id=org_id,
                role_name=Role.ORG_ADMIN.name,
            )
            user_id = await self.user_repo.create_user_tx(user, conn)
            return user_id

        try:
            user_id = await self.user_repo.execute_transaction(tx)
        except asyncpg.UniqueViolationError:
            raise EmailAlreadyExists()
        except Exception as ex:
            logger.error(ex)
            raise SignupFailed()

        await self.email_verification_service.send_verification_email(
            user_id=user_id, email=data.email
        )

        return SignupResult(user_id=user_id)

    async def verify_credentials(self, email: str, password: str) -> User | None:
        user_with_pw: UserWithPassword = (
            await self.user_repo.get_user_with_password_by_email(email)
        )

        if not user_with_pw:
            return None

        if not verify_password_hash(user_with_pw.password_hash, password):
            return None

        return User(**user_with_pw.model_dump())

    async def _link_oauth_to_existing_user(
        self, existing_user: User, provider_id: str, provider_user_id: str, avatar_url: str
    ) -> User:
        """
        Link OAuth account to existing user and update avatar if needed.
        
        Args:
            existing_user: Existing user to link OAuth account to
            provider_id: OAuth provider ID (e.g., "google")  
            provider_user_id: User ID from OAuth provider
            avatar_url: Avatar URL from OAuth provider
            
        Returns:
            User: The existing user with linked OAuth account
            
        Raises:
            SignupFailed: If linking fails
        """
        try:
            await self.user_repo.create_oauth_account(
                existing_user.id, provider_id, provider_user_id
            )
            # Update user profile with OAuth data if missing
            if avatar_url:
                await self.user_repo.update_user_avatar_if_null(existing_user.id, avatar_url)
            
            logger.info(f"Linked OAuth account to existing user: {existing_user.email}")
            return existing_user
        except Exception as e:
            logger.error(f"Failed to link OAuth account to existing user: {e}")
            raise SignupFailed("Failed to link Google account to existing user")

    async def _create_new_oauth_user(
        self, email: str, first_name: str, last_name: str, avatar_url: str, 
        provider_id: str, provider_user_id: str
    ) -> User:
        """
        Create a new user from OAuth information.
        
        Args:
            email: User email from OAuth provider
            first_name: User first name from OAuth provider
            last_name: User last name from OAuth provider
            avatar_url: Avatar URL from OAuth provider
            provider_id: OAuth provider ID (e.g., "google")
            provider_user_id: User ID from OAuth provider
            
        Returns:
            User: Newly created user
            
        Raises:
            SignupFailed: If user creation fails
        """
        async def tx(conn):
            org_name = f"{email}'s Organization"
            org_id = await self.org_repo.create_organization_tx(org_name, conn)

            role_name = (
                Role.ORG_ADMIN.name if settings.mode == "b2c" else Role.MEMBER.name
            )

            user = CreateUser(
                email=email,
                password_hash=None,
                first_name=first_name,
                last_name=last_name,
                organization_id=org_id,
                role_name=role_name,
                email_verified=True,
                email_verified_at=datetime.now(timezone.utc),
                avatar_url=avatar_url,
            )
            user_id = await self.user_repo.create_user_tx(user, conn)
            await self.user_repo.create_oauth_account_tx(
                conn, provider_id, provider_user_id, user_id
            )
            return user_id

        try:
            user_id = await self.user_repo.execute_transaction(tx)
        except Exception as e:
            logger.error(f"OAuth signup failed: {e}")
            raise SignupFailed()

        return await self.user_repo.get_user_by_id(user_id)

    async def login_with_google(self, auth_code: str) -> User:
        from app.util.oauth_util import exchange_oauth_code_for_user_info
        
        # Get user info from OAuth provider
        id_info = await exchange_oauth_code_for_user_info(auth_code)

        # Extract user information from ID token
        provider_id = "google"
        provider_user_id = id_info["sub"]
        email = id_info["email"]
        first_name = id_info.get("given_name", "")
        last_name = id_info.get("family_name", "")
        avatar_url = id_info.get("picture")

        # Check if user already has OAuth account linked
        existing_oauth_user = await self.user_repo.get_user_by_oauth(
            provider_id, provider_user_id
        )
        if existing_oauth_user:
            return existing_oauth_user

        # Check if a user already exists with this email (password-based account)
        existing_email_user = await self.user_repo.get_user_by_email(email)
        if existing_email_user:
            return await self._link_oauth_to_existing_user(
                existing_email_user, provider_id, provider_user_id, avatar_url
            )

        # Create new user with OAuth account
        return await self._create_new_oauth_user(
            email, first_name, last_name, avatar_url, provider_id, provider_user_id
        )

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
