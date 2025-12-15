from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel, BigInt


class UserModel(BaseModel):
    __tablename__ = "users"

    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None] = mapped_column(unique=True, index=True)
    telegram_id: Mapped[BigInt] = mapped_column(unique=True, index=True)
    stars: Mapped[int] = mapped_column(server_default="0")
    tickets: Mapped[int] = mapped_column(server_default="0")

    def __str__(self) -> str:
        return f"User: {self.id}. Telegram ID: {self.telegram_id}"
