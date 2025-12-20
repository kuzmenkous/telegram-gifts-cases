from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, NonNegativeInt, PositiveInt

from src.domain.base import IdSchema, OrderByBase


class StarsTicketsMixin(BaseModel):
    stars: NonNegativeInt
    tickets: NonNegativeInt


class UserPreview(StarsTicketsMixin, IdSchema):
    first_name: str
    last_name: str | None = None
    username: str | None = None
    telegram_id: PositiveInt
    photo_url: str | None = None
    created_at: datetime


class UserRead(UserPreview):
    referrals_count: NonNegativeInt


class UserUpdate(StarsTicketsMixin, BaseModel):
    pass


@dataclass
class UserFilters:
    first_name__ilike: str | None = None
    last_name__ilike: str | None = None
    username__ilike: str | None = None
    telegram_id: PositiveInt | None = None
    stars__ge: NonNegativeInt | None = None


type OrderBy = OrderByBase[
    Literal["username", "stars", "tickets", "created_at"]
]
