from app.data.repo.user_repo import UserRepo
from app.model.user_model import User


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def list_users(self) -> list[User]:
        return await self.user_repo.list_users()
