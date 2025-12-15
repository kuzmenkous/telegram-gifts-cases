from typing import Annotated

from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, Depends

from src.dependencies.db import Session
from src.dependencies.user import get_verified_and_parsed_init_data
from src.domain.user import UserRead
from src.services.user import UserService

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/auth")
async def users_auth(
    init_data: Annotated[
        WebAppInitData, Depends(get_verified_and_parsed_init_data)
    ],
    session: Session,
) -> UserRead:
    user_model = await UserService(session).get_or_create_user_with_init_data(
        init_data.user  # type: ignore[arg-type]
    )
    return UserRead.model_validate(user_model)
