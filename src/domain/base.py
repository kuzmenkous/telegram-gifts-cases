from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any, Literal

from annotated_types import Interval
from pydantic import BaseModel, NonNegativeInt, PositiveInt, field_validator


class IsActiveMixin(BaseModel):
    is_active: bool


class CreatedAtMixin:
    created_at: datetime


class IdSchema(BaseModel, from_attributes=True):
    id: PositiveInt


@dataclass
class Pagination:
    offset: NonNegativeInt = 0
    limit: Annotated[int, Interval(ge=10, le=500)] = 50


class Page[I: Iterable[Any]](BaseModel):
    items: I
    pagination: Pagination
    total: NonNegativeInt


class ItemsPage[Item](Page[list[Item]]):
    @field_validator("items", mode="before")
    @classmethod
    def convert_items(cls, value: Any) -> Any:
        if isinstance(value, Iterable) and not isinstance(value, list):
            return list(value)
        return value


type OrderByBase[Fields] = dict[Fields, Literal["asc", "desc"]]
