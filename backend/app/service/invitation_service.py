import secrets
from datetime import datetime, timedelta, timezone

from app.config.settings import settings
from app.data.repo.invitation_repo import InvitationRepo
from app.data.repo.organization_repo import OrganizationRepo
from app.data.repo.user_repo import UserRepo
from app.model.invitation_model import Invitation
from app.model.user_model import CreateUser
from app.util.hash_util import hash_password


class InvitationService:
    def __init__(
        self,
        invitation_repo: InvitationRepo,
        user_repo: UserRepo,
        org_repo: OrganizationRepo,
    ):
        self.invitation_repo = invitation_repo
        self.user_repo = user_repo
        self.org_repo = org_repo

    async def create_invitation(
        self,
        email: str,
        role: str,
        organization_id: int,
        created_by: int | None,
    ) -> tuple[Invitation, str]:
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.invitation_expiry_days
        )

        invitation = await self.invitation_repo.create_invitation(
            email=email,
            role_name=role,
            organization_id=organization_id,
            created_by=created_by,
            token=token,
            expires_at=expires_at,
        )

        invite_link = f"{settings.base_web_url}/invite/accept?token={token}"
        return invitation, invite_link

    async def get_pending_invitations(self, organization_id: int) -> list[Invitation]:
        return await self.invitation_repo.get_pending_invitations(organization_id)

    async def get_invitation(
        self, invitation_id: int, organization_id: int
    ) -> Invitation:
        return await self.invitation_repo.get_invitation_by_id(
            invitation_id, organization_id
        )

    async def revoke_invitation(self, invitation_id: int, organization_id: int) -> None:
        await self.invitation_repo.revoke_invitation(invitation_id, organization_id)

    async def accept_invitation(
        self,
        token: str,
        password: str,
        first_name: str | None,
        last_name: str | None,
        organization_name: str | None,
    ) -> bool:
        invitation = await self.invitation_repo.get_valid_invitation_by_token(token)
        if not invitation:
            return False

        password_hash = hash_password(password)
        now = datetime.now(timezone.utc)

        async def tx(conn):
            if invitation.organization_id:
                org_id = invitation.organization_id
            else:
                name = organization_name or f"{invitation.email}'s Organization"
                org_id = await self.org_repo.create_organization_tx(name, conn)

            user = CreateUser(
                email=invitation.email,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
                organization_id=org_id,
                role_name=invitation.role_name,
                email_verified=True,
                email_verified_at=now,
            )

            await self.user_repo.create_user_tx(user, conn)
            await self.invitation_repo.mark_invitation_as_accepted_tx(
                invitation.id, conn
            )

        await self.invitation_repo.execute_transaction(tx)
        return True

    async def get_all_pending_invitations(self) -> list[Invitation]:
        return await self.invitation_repo.get_all_pending_invitations()
