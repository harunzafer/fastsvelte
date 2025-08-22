from app.data.repo.user_repo import UserRepo
from app.model.user_model import User


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def list_users(self) -> list[User]:
        return await self.user_repo.list_users()

    async def update_user_info(
        self, user_id: int, first_name: str | None, last_name: str | None
    ) -> None:
        await self.user_repo.update_user_name(user_id, first_name, last_name)

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repo.get_user_by_id(user_id)

    async def update_user_avatar(self, user_id: int, avatar_data: str) -> None:
        await self.user_repo.update_user_avatar(user_id, avatar_data)
