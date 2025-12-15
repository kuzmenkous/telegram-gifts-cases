from typing import Annotated

from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, Body, Depends
from pydantic.json_schema import SkipJsonSchema

from src.dependencies.admin import get_admin_by_api_token, get_superadmin
from src.dependencies.db import Session
from src.dependencies.user import (
    get_current_user,
    get_user_model,
    get_verified_and_parsed_init_data,
)
from src.domain.base import ItemsPage, Pagination
from src.domain.constants.api import openapi_extra_for_pagination
from src.domain.user import OrderBy, UserFilters, UserRead, UserUpdate
from src.models.user import UserModel
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


@users_router.get("/me")
async def users_me(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserRead:
    return UserRead.model_validate(current_user)


@users_router.post(
    "/list",
    dependencies=(Depends(get_admin_by_api_token),),
    openapi_extra=openapi_extra_for_pagination,
)
async def get_users(
    filters: Annotated[UserFilters, Depends()],
    pagination: Annotated[Pagination, Depends()],
    session: Session,
    order_by: Annotated[
        OrderBy | SkipJsonSchema[None], Body(min_length=1)
    ] = None,
) -> ItemsPage[UserRead]:
    if order_by is None or len(order_by) == 0:
        order_by = {"created_at": "desc"}

    return await UserService(session).get_users(filters, pagination, order_by)


@users_router.get(
    "/{user_id}", dependencies=(Depends(get_admin_by_api_token),)
)
async def get_user(
    user_model: Annotated[UserModel, Depends(get_user_model)],
) -> UserRead:
    return UserRead.model_validate(user_model)


@users_router.put("/update", dependencies=(Depends(get_superadmin),))
async def update_user(
    user_update: UserUpdate,
    user_model: Annotated[UserModel, Depends(get_user_model)],
) -> None:
    for field_name, value in user_update.model_dump().items():
        setattr(user_model, field_name, value)
