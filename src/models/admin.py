from uuid import UUID

from sqlalchemy import ForeignKey, false, text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel


class AdminModel(BaseModel):
    __tablename__ = "admins"

    username: Mapped[str] = mapped_column(unique=True, index=True)
    is_superadmin: Mapped[bool] = mapped_column(server_default=false())
    hashed_password: Mapped[str]

    def __str__(self) -> str:
        return f"Admin: {self.username}. ID: {self.id}"


class SessionModel(BaseModel):
    __tablename__ = "sessions"

    token: Mapped[UUID] = mapped_column(
        unique=True, server_default=text("gen_random_uuid()")
    )
    admin_id: Mapped[int] = mapped_column(
        ForeignKey("admins.id", ondelete="CASCADE"), index=True
    )

    def __str__(self) -> str:
        return f"Session: {self.token}. Admin ID: {self.admin_id}"
