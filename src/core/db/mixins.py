from sqlalchemy import true
from sqlalchemy.orm import Mapped, mapped_column


class IsActiveMixin:
    is_active: Mapped[bool] = mapped_column(
        server_default=true(), sort_order=99
    )
