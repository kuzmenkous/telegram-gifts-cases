import time
from typing import Annotated

from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data
from fastapi import Depends, Header, HTTPException, status
from pydantic import PositiveInt

from src.core.config import settings
from src.dependencies.db import Session
from src.models.user import UserModel
from src.repositories.user import UserRepository


async def get_verified_and_parsed_init_data(
    init_data: str = Header(..., alias="Authorization")
) -> WebAppInitData:
    try:
        parsed_data = safe_parse_webapp_init_data(
            settings.telegram.bot_token, init_data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid init data signature",
        ) from e

    current_timestamp = int(time.time())
    auth_timestamp = int(parsed_data.auth_date.timestamp())
    age_seconds = current_timestamp - auth_timestamp

    if age_seconds > settings.telegram.init_data_expire:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Init data has expired",
        )

    return parsed_data


async def get_current_user(
    init_data: Annotated[
        WebAppInitData, Depends(get_verified_and_parsed_init_data)
    ],
    session: Session,
) -> UserModel:
    user_model = await UserRepository(session).get_by_telegram_id(
        init_data.user.id  # type: ignore[union-attr]
    )
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return user_model


async def get_user_model(user_id: PositiveInt, session: Session) -> UserModel:
    return await session.get_one(UserModel, user_id)
