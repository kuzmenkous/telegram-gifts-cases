from collections.abc import Iterable

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement


class Repository[T]:
    def __init__(self, model: type[T]) -> None:
        self.model = model

    async def get_one(
        self, session: AsyncSession, conditions: Iterable[ColumnElement[bool]]
    ) -> T:
        stmt = select(self.model).where(*conditions)
        return (await session.execute(stmt)).scalar_one()

    async def get_all(
        self,
        session: AsyncSession,
        conditions: Iterable[ColumnElement[bool]] | None = None,
    ) -> tuple[T, ...]:
        stmt = select(self.model)
        if conditions:
            stmt = stmt.where(*conditions)
        return tuple(await session.scalars(stmt))

    async def exists(
        self, session: AsyncSession, conditions: Iterable[ColumnElement[bool]]
    ) -> bool:
        stmt = exists().where(*conditions).select()
        return (await session.execute(stmt)).scalar_one()
