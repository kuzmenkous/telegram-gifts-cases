from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound

from src.domain.admin import (
    AdminCreate,
    AdminCredentials,
    AdminFilters,
    AdminRead,
    OrderBy,
)
from src.domain.base import ItemsPage, Pagination
from src.domain.constants.admin import password_hasher
from src.models.admin import AdminModel, SessionModel
from src.queries.admin import get_select_admins_query
from src.queries.base import get_select_total_query
from src.repositories.admin import AdminRepository, SessionRepository
from src.services.base import BaseService


class AdminService(BaseService):
    async def get_admin_by_credentials(
        self, credentials: AdminCredentials
    ) -> AdminModel:
        try:
            admin_model = await AdminRepository(
                self._session
            ).get_admin_by_username(credentials.username)
            password_hasher.verify(
                admin_model.hashed_password,
                credentials.password.get_secret_value(),
            )
        except (NoResultFound, VerifyMismatchError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        if password_hasher.check_needs_rehash(admin_model.hashed_password):
            admin_model.hashed_password = password_hasher.hash(
                credentials.password.get_secret_value()
            )
            self._session.add(admin_model)
            await self._session.commit()
        return admin_model

    async def create_admin(self, admin_create: AdminCreate) -> int:
        admin_model = AdminModel(
            username=admin_create.username,
            hashed_password=admin_create.hashed_password,
        )
        self._session.add(admin_model)
        await self._session.flush()

        return admin_model.id

    async def get_admin_by_id(self, admin_id: int) -> AdminModel:
        return await AdminRepository(self._session).get_admin(admin_id)

    async def get_admins(
        self, filters: AdminFilters, pagination: Pagination, order_by: OrderBy
    ) -> ItemsPage[AdminRead]:
        return ItemsPage[AdminRead](
            items=(
                await AdminRepository(self._session).get_admins(
                    filters, pagination, order_by
                )
            ),
            total=(
                await self._session.execute(
                    get_select_total_query(get_select_admins_query(filters))
                )
            ).scalar_one(),
            pagination=pagination,
        )

    async def delete_admin(self, admin_id: int) -> None:
        await AdminRepository(self._session).delete_admin(admin_id)


class SessionService(BaseService):
    async def get_session_by_token(self, token: UUID) -> SessionModel:
        session_model = await SessionRepository(
            self._session
        ).get_session_by_token(token)
        if not session_model:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return session_model

    async def delete_session_by_token(self, token: UUID) -> None:
        await SessionRepository(self._session).delete_session_by_token(token)
