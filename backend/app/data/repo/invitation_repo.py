from datetime import datetime
from typing import Optional

from app.data.repo.base_repo import BaseRepo
from app.model.invitation_model import Invitation


class InvitationRepo(BaseRepo):
    async def create_invitation(
        self,
        email: str,
        role_name: str,
        organization_id: int,
        created_by: int | None,
        token: str,
        expires_at: datetime,
    ) -> Invitation:
        query = """
            INSERT INTO fastsvelte.invitation (
                email, token, role_name, organization_id, created_by, expires_at
            )
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
        """
        row = await self.fetch_one(
            query, email, token, role_name, organization_id, created_by, expires_at
        )
        return Invitation(**row)

    async def get_pending_invitations(self, organization_id: int) -> list[Invitation]:
        query = """
            SELECT * FROM fastsvelte.invitation
            WHERE organization_id = $1 AND accepted_at IS NULL
            ORDER BY created_at DESC
        """
        rows = await self.fetch_all(query, organization_id)
        return [Invitation(**row) for row in rows]

    async def get_invitation_by_id(
        self, invitation_id: int, organization_id: int
    ) -> Optional[Invitation]:
        query = """
            SELECT * FROM fastsvelte.invitation
            WHERE id = $1 AND organization_id = $2
        """
        row = await self.fetch_one(query, invitation_id, organization_id)
        return Invitation(**row) if row else None

    async def get_valid_invitation_by_token(self, token: str) -> Optional[Invitation]:
        query = """
            SELECT * FROM fastsvelte.invitation
            WHERE token = $1 AND accepted_at IS NULL AND expires_at > now()
        """
        row = await self.fetch_one(query, token)
        return Invitation(**row) if row else None

    async def mark_invitation_as_accepted(self, invitation_id: int) -> None:
        query = """
            UPDATE fastsvelte.invitation
            SET accepted_at = now()
            WHERE id = $1
        """
        await self.execute(query, invitation_id)

    async def mark_invitation_as_accepted_tx(self, invitation_id: int, conn) -> None:
        query = """
            UPDATE fastsvelte.invitation
            SET accepted_at = now()
            WHERE id = $1
        """
        await conn.execute(query, invitation_id)

    async def revoke_invitation(self, invitation_id: int, organization_id: int) -> bool:
        query = """
            DELETE FROM fastsvelte.invitation
            WHERE id = $1 AND organization_id = $2 AND accepted_at IS NULL
        """
        rows = await self.fetch_all(query, invitation_id, organization_id)
        print(
            f"Rows deleted: {len(rows)} for invitation_id: {invitation_id}, organization_id: {organization_id}"
        )
        return len(rows) > 0

    async def get_all_pending_invitations(self) -> list[Invitation]:
        query = """
            SELECT * FROM fastsvelte.invitation
            WHERE accepted_at IS NULL
            ORDER BY created_at DESC
        """
        rows = await self.fetch_all(query)
        return [Invitation(**row) for row in rows]
