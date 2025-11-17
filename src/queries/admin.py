from sqlalchemy import Select, select

from src.domain.admin import AdminFilters
from src.models.admin import AdminModel

_select_admins_query = select(AdminModel)


def get_select_admins_query(
    filters: AdminFilters,
) -> Select[tuple[AdminModel]]:
    stmt = _select_admins_query
    if filters.username__ilike is not None:
        stmt = stmt.where(
            AdminModel.username.ilike(f"%{filters.username__ilike}%")
        )
    if filters.is_superadmin is not None:
        stmt = stmt.where(AdminModel.is_superadmin.is_(filters.is_superadmin))
    return stmt
