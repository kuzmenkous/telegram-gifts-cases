from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, query_expression

from src.models.base import BaseModel, BigInt, Id


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[Id]
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None] = mapped_column(unique=True, index=True)
    telegram_id: Mapped[BigInt] = mapped_column(unique=True, index=True)
    photo_url: Mapped[str | None]
    stars: Mapped[int] = mapped_column(server_default="0")
    tickets: Mapped[int] = mapped_column(server_default="0")

    referrer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE")
    )

    referrals_count: Mapped[int | None] = query_expression()

    def __str__(self) -> str:
        return f"User: {self.id}. Telegram ID: {self.telegram_id}"
