from datetime import datetime

from pydantic import NonNegativeInt, PositiveInt

from src.domain.base import IdSchema


class UserRead(IdSchema):
    first_name: str
    last_name: str | None
    username: str | None
    telegram_id: PositiveInt
    stars: NonNegativeInt
    tickets: NonNegativeInt
    created_at: datetime
