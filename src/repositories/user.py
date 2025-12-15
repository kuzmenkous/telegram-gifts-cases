from sqlalchemy import select

from src.models.user import UserModel
from src.repositories.base import Repository


class UserRepository(Repository):
    async def get_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        return (
            await self._session.execute(
                select(UserModel).where(UserModel.telegram_id == telegram_id)
            )
        ).scalar_one_or_none()
