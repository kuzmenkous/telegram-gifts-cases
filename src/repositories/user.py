from sqlalchemy import select

from src.domain.base import Pagination
from src.domain.user import OrderBy, UserFilters
from src.models.user import UserModel
from src.queries.base import add_order_by_and_offset_limit_to_query
from src.queries.user import get_select_users_query
from src.repositories.base import Repository


class UserRepository(Repository):
    async def get_users(
        self, filters: UserFilters, pagination: Pagination, order_by: OrderBy
    ) -> tuple[UserModel, ...]:
        select_query_with_filters = get_select_users_query(filters)
        return tuple(
            await self._session.scalars(
                add_order_by_and_offset_limit_to_query(
                    select_query_with_filters, order_by, pagination
                )
            )
        )

    async def get_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        return (
            await self._session.execute(
                select(UserModel).where(UserModel.telegram_id == telegram_id)
            )
        ).scalar_one_or_none()
