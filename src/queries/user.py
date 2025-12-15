from sqlalchemy import Select, select

from src.domain.user import UserFilters
from src.models.user import UserModel

_select_users_query = select(UserModel)


def get_select_users_query(filters: UserFilters) -> Select[tuple[UserModel]]:
    stmt = _select_users_query
    if filters.first_name__ilike is not None:
        stmt = stmt.where(
            UserModel.first_name.ilike(f"%{filters.first_name__ilike}%")
        )
    if filters.last_name__ilike is not None:
        stmt = stmt.where(
            UserModel.last_name.ilike(f"%{filters.last_name__ilike}%")
        )
    if filters.username__ilike is not None:
        stmt = stmt.where(
            UserModel.username.ilike(f"%{filters.username__ilike}%")
        )
    if filters.telegram_id is not None:
        stmt = stmt.where(UserModel.telegram_id == filters.telegram_id)
    if filters.stars__ge is not None:
        stmt = stmt.where(UserModel.stars >= filters.stars__ge)
    return stmt
