from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from src.domain.admin import AdminCreate, _PasswordForCheck
from src.models.admin import AdminModel


class SuperadminCredentials(AdminCreate, BaseSettings):
    username: Annotated[str, Field(validation_alias="SUPERADMIN_USERNAME")]
    password: Annotated[
        _PasswordForCheck, Field(validation_alias="SUPERADMIN_PASSWORD")
    ]
    password2: Annotated[
        _PasswordForCheck, Field(validation_alias="SUPERADMIN_PASSWORD")
    ]


superadmin_credentials = SuperadminCredentials()


async def insert_first_rows_with_async_connection(
    async_connection: AsyncConnection,
) -> None:
    session = AsyncSession(async_connection)
    await create_first_rows(session)
    await session.flush()


async def create_first_rows(session: AsyncSession) -> None:
    # Create superadmin
    user = AdminModel(
        username=superadmin_credentials.username,
        is_superadmin=True,
        hashed_password=superadmin_credentials.hashed_password,
    )
    session.add(user)
