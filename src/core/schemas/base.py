from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any, TypeVar

from annotated_types import Interval
from pydantic import BaseModel, NonNegativeInt, PositiveInt, field_validator
from pydantic_extra_types.timezone_name import (
    TimeZoneName,
    timezone_name_settings,
)

Model = TypeVar("Model", bound=BaseModel)


class IsActiveMixin:
    is_active: bool


class CreatedAtMixin:
    created_at: datetime


class IdSchema(BaseModel, from_attributes=True):
    id: PositiveInt


class NameMixin:
    name: str


class IdNameSchema(NameMixin, IdSchema):
    pass


@timezone_name_settings(strict=False)
class TimeZoneNameNonStrict(TimeZoneName):
    pass


@dataclass
class Pagination:
    offset: NonNegativeInt = 0
    limit: Annotated[int, Interval(ge=10, le=500)] = 50


class Page[I: Iterable[Any]](BaseModel):
    items: I
    pagination: Pagination
    total: int


class DictPage[Item](Page[dict[PositiveInt, Item]]):
    @field_validator("items", mode="before")
    @classmethod
    def convert_items(cls, value: Any) -> Any:
        if isinstance(value, Iterable) and not isinstance(value, dict):
            return {item.id: item for item in value}
        return value
