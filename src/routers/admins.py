from typing import Annotated, Literal

from fastapi import APIRouter, Body, Depends, Path, status
from pydantic import PositiveInt
from pydantic.json_schema import SkipJsonSchema

from src.dependencies.admin import (
    LoggedInAdmin,
    get_admin_by_api_token,
    get_admin_model,
    get_superadmin,
)
from src.dependencies.db import Session
from src.domain.admin import (
    AdminCreate,
    AdminFilters,
    AdminRead,
    AdminUpdate,
    OrderBy,
)
from src.domain.base import ItemsPage, Pagination
from src.domain.constants.api import openapi_extra_for_pagination
from src.models.admin import AdminModel
from src.services.admin import AdminService

admins_router = APIRouter(prefix="/admins", tags=["Admins"])


@admins_router.post(
    "",
    dependencies=(Depends(get_superadmin),),
    status_code=status.HTTP_201_CREATED,
    response_description="ID of the created admin",
)
async def create_admin(session: Session, admin_create: AdminCreate) -> int:
    return await AdminService(session).create_admin(admin_create)


@admins_router.post(
    "/list",
    dependencies=(Depends(get_admin_by_api_token),),
    openapi_extra=openapi_extra_for_pagination,
)
async def get_admins(
    filters: Annotated[AdminFilters, Depends()],
    pagination: Annotated[Pagination, Depends()],
    session: Session,
    order_by: Annotated[
        OrderBy | SkipJsonSchema[None], Body(min_length=1)
    ] = None,
) -> ItemsPage[AdminRead]:
    if order_by is None or len(order_by) == 0:
        order_by = {"created_at": "desc"}

    return await AdminService(session).get_admins(
        filters, pagination, order_by
    )


@admins_router.get("/{admin_id_or_me}")
async def get_admin(
    session: Session,
    logged_in_admin: LoggedInAdmin,
    admin_id_or_me: Annotated[PositiveInt | Literal["me"], Path()],
) -> AdminRead:
    if admin_id_or_me == "me":
        return AdminRead.model_validate(logged_in_admin)

    admin_model = await AdminService(session).get_admin_by_id(admin_id_or_me)
    return AdminRead.model_validate(admin_model)


@admins_router.put(
    "/{admin_id}",
    dependencies=(Depends(get_superadmin),),
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_admin(
    admin_model: Annotated[AdminModel, Depends(get_admin_model)],
    admin_update: AdminUpdate,
) -> None:
    for field_name, value in admin_update.model_dump().items():
        setattr(admin_model, field_name, value)


@admins_router.delete(
    "/{admin_id}",
    dependencies=(Depends(get_superadmin),),
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_admin(session: Session, admin_id: PositiveInt) -> None:
    await AdminService(session).delete_admin(admin_id)
