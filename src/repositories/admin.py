from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.admin import AdminModel, SessionModel
from src.repositories.base import Repository


class AdminRepository:
    _repository: Repository[AdminModel] = Repository(AdminModel)

    async def get_admin(
        self, session: AsyncSession, admin_id: int
    ) -> AdminModel:
        return await session.get_one(AdminModel, admin_id)

    async def get_admin_by_username(
        self, session: AsyncSession, username: str
    ) -> AdminModel:
        return await self._repository.get_one(
            session, (AdminModel.username == username,)
        )

    async def delete_admin(self, session: AsyncSession, admin_id: int) -> None:
        stmt = delete(AdminModel).where(AdminModel.id == admin_id)
        await session.execute(stmt)


class SessionRepository:
    _repository: Repository[SessionModel] = Repository(SessionModel)

    async def get_session_by_token(
        self, session: AsyncSession, token: UUID
    ) -> SessionModel | None:
        stmt = (
            select(SessionModel)
            .where(SessionModel.token == token)
            .options(joinedload(SessionModel.admin, innerjoin=True))
        )
        return (await session.execute(stmt)).scalar_one_or_none()

    async def delete_session_by_token(
        self, session: AsyncSession, token: UUID
    ) -> None:
        stmt = delete(SessionModel).where(SessionModel.token == token)
        await session.execute(stmt)
