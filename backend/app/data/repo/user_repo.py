import logging
from typing import Optional

from app.data.repo.base_repo import BaseRepo
from app.model.role_model import Role
from app.model.user_model import CreateUser, User, UserWithPassword, UserWithRole

logger = logging.getLogger(__name__)


class UserRepo(BaseRepo):
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = """
            SELECT id, email, first_name, last_name,
                email_verified, email_verified_at,
                is_active, deleted_at,
                organization_id, role_id,
                created_at, updated_at
            FROM fastsvelte."user"
            WHERE id = $1 AND deleted_at IS NULL
        """
        row = await self.fetch_one(query, user_id)
        return User(**row) if row else None

    async def list_users(self) -> list[User]:
        query = """
            SELECT
                id, email, first_name, last_name,
                email_verified, email_verified_at,
                is_active, deleted_at,
                organization_id, role_id,
                created_at, updated_at
            FROM fastsvelte."user"
            WHERE deleted_at IS NULL
        """
        rows = await self.fetch_all(query)
        return [User(**row) for row in rows]

    async def get_user_with_password_by_email(
        self, email: str
    ) -> Optional[UserWithPassword]:
        query = """
            SELECT
                id, email, password_hash, first_name, last_name,
                email_verified, email_verified_at,
                is_active, deleted_at,
                organization_id, role_id,
                created_at, updated_at
            FROM fastsvelte."user"
            WHERE email = $1 AND deleted_at IS NULL
        """
        row = await self.fetch_one(query, email)
        return UserWithPassword(**row) if row else None

    async def create_user(self, data: CreateUser) -> int:
        row = await self.fetch_one(
            self._create_user_query(),
            data.email,
            data.password_hash,
            data.first_name,
            data.last_name,
            data.organization_id,
            data.role_name,
            data.email_verified,
            data.email_verified_at,
        )
        return row["id"]

    async def create_user_tx(self, data: CreateUser, conn) -> int:
        row = await conn.fetchrow(
            self._create_user_query(),
            data.email,
            data.password_hash,
            data.first_name,
            data.last_name,
            data.organization_id,
            data.role_name,
            data.email_verified,
            data.email_verified_at,
        )
        return row["id"]

    def _create_user_query(self) -> str:
        return """
            INSERT INTO fastsvelte."user" (
                email, password_hash, first_name, last_name,
                organization_id, role_id,
                email_verified, email_verified_at
            )
            VALUES (
                $1, $2, $3, $4,
                $5,
                (SELECT id FROM fastsvelte.role WHERE name = $6),
                $7, $8
            )
            RETURNING id
        """

    async def get_user_with_role_by_id(self, user_id: int) -> Optional[UserWithRole]:
        query = """
            SELECT
                u.id, u.email, u.first_name, u.last_name,
                u.email_verified, u.email_verified_at,
                u.is_active, u.deleted_at,
                u.organization_id, u.role_id,
                u.created_at, u.updated_at,
                r.name AS role_name
            FROM fastsvelte."user" u
            LEFT JOIN fastsvelte.role r ON u.role_id = r.id
            WHERE u.id = $1 AND u.deleted_at IS NULL
        """
        row = await self.fetch_one(query, user_id)
        try:
            role = Role.get(row["role_name"])
        except KeyError:
            logger.error(f"Unknown role '{row['role_name']}' for user_id={user_id}")
            return None

        return UserWithRole(**row, role=role)

    async def get_user_by_email(self, email: str) -> User | None:
        query = """
            SELECT id, email, first_name, last_name, organization_id, is_active, deleted_at,
                created_at, updated_at, role_id
            FROM fastsvelte."user"
            WHERE email = $1
        """
        row = await self.fetch_one(query, email)
        return User(**row) if row else None

    async def update_user_name(
        self, user_id: int, first_name: str | None, last_name: str | None
    ) -> None:
        updates = []
        params = [user_id]

        if first_name is not None:
            updates.append("first_name = $" + str(len(params) + 1))
            params.append(first_name)

        if last_name is not None:
            updates.append("last_name = $" + str(len(params) + 1))
            params.append(last_name)

        if not updates:
            return  # nothing to update

        updates.append("updated_at = now()")
        query = f"""
            UPDATE fastsvelte."user"
            SET {", ".join(updates)}
            WHERE id = $1 AND deleted_at IS NULL
        """
        await self.execute(query, *params)

    async def get_user_by_oauth(
        self, provider_id: str, provider_user_id: str
    ) -> User | None:
        query = """
            SELECT u.id, u.email, u.first_name, u.last_name, u.avatar_url,
                   u.email_verified, u.email_verified_at,
                   u.is_active, u.deleted_at,
                   u.organization_id, u.role_id,
                   u.created_at, u.updated_at
            FROM fastsvelte.oauth_account oa
            JOIN fastsvelte."user" u ON oa.user_id = u.id
            WHERE oa.provider_id = $1 AND oa.provider_user_id = $2
              AND u.deleted_at IS NULL
        """
        row = await self.fetch_one(query, provider_id, provider_user_id)
        return User(**row) if row else None

    async def create_oauth_account(
        self, user_id: int, provider_id: str, provider_user_id: str
    ) -> None:
        query = """
            INSERT INTO fastsvelte.oauth_account (user_id, provider_id, provider_user_id)
            VALUES ($1, $2, $3)
            ON CONFLICT DO NOTHING
        """
        await self.execute(query, user_id, provider_id, provider_user_id)
