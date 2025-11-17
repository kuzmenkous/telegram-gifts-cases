from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from src.domain.admin import AdminFilters, OrderBy
from src.domain.base import Pagination
from src.models.admin import AdminModel, SessionModel
from src.queries.admin import get_select_admins_query
from src.queries.base import add_order_by_and_offset_limit_to_query
from src.repositories.base import Repository


class AdminRepository(Repository):
    async def get_admin(self, admin_id: int) -> AdminModel:
        return await self._session.get_one(AdminModel, admin_id)

    async def get_admin_by_username(self, username: str) -> AdminModel:
        stmt = select(AdminModel).where(AdminModel.username == username)
        return (await self._session.execute(stmt)).scalar_one()

    async def get_admins(
        self, filters: AdminFilters, pagination: Pagination, order_by: OrderBy
    ) -> tuple[AdminModel, ...]:
        select_query_with_filters = get_select_admins_query(filters)
        return tuple(
            await self._session.scalars(
                add_order_by_and_offset_limit_to_query(
                    select_query_with_filters, order_by, pagination
                )
            )
        )

    async def delete_admin(self, admin_id: int) -> None:
        await self._session.execute(
            delete(AdminModel).where(AdminModel.id == admin_id)
        )


class SessionRepository(Repository):
    async def get_session_by_token(self, token: UUID) -> SessionModel | None:
        stmt = (
            select(SessionModel)
            .where(SessionModel.token == token)
            .options(joinedload(SessionModel.admin, innerjoin=True))
        )
        return (await self._session.execute(stmt)).scalar_one_or_none()

    async def delete_session_by_token(self, token: UUID) -> None:
        await self._session.execute(
            delete(SessionModel).where(SessionModel.token == token)
        )
