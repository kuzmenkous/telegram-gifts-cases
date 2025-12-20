from aiogram.utils.web_app import WebAppUser

from src.domain.base import ItemsPage, Pagination
from src.domain.user import OrderBy, UserFilters, UserRead
from src.models.user import UserModel
from src.queries.base import get_select_total_query
from src.queries.user import get_select_users_query
from src.repositories.user import UserRepository
from src.services.base import BaseService


class UserService(BaseService):
    async def get_or_create_user_with_init_data(
        self, web_app_user: WebAppUser
    ) -> UserModel:
        user_model = await UserRepository(self._session).get_by_telegram_id(
            web_app_user.id
        )
        if not user_model:
            user_model = UserModel(
                telegram_id=web_app_user.id,
                first_name=web_app_user.first_name,
                last_name=web_app_user.last_name,
                username=web_app_user.username,
            )
            self._session.add(user_model)
            await self._session.flush()
        return user_model

    async def get_users(
        self, filters: UserFilters, pagination: Pagination, order_by: OrderBy
    ) -> ItemsPage[UserRead]:
        return ItemsPage[UserRead](
            items=(
                await UserRepository(self._session).get_users(
                    filters, pagination, order_by
                )
            ),
            total=(
                await self._session.execute(
                    get_select_total_query(get_select_users_query(filters))
                )
            ).scalar_one(),
            pagination=pagination,
        )
