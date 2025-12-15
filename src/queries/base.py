from collections.abc import Iterable
from operator import attrgetter
from typing import Any

from sqlalchemy import Select, func

from src.domain.base import Pagination
from src.models.base import BaseModel


def get_select_total_query(
    stmt: Select[tuple[Any, ...]],
) -> Select[tuple[int]]:
    return stmt.with_only_columns(func.count(), maintain_column_froms=True)


def add_order_by_to_query[M: BaseModel](
    stmt: Select[tuple[M]], order_by: dict[Any, Any]
) -> Select[tuple[M]]:
    model = stmt.column_descriptions[0]["expr"]
    getter_of_direction_methods_of_fields = attrgetter(
        *(
            f"{field_name.replace('.', '.mapper.class_.')}.{direction_name}"
            for field_name, direction_name in order_by.items()
        )
    )
    direction_methods_of_fields = getter_of_direction_methods_of_fields(model)
    if not isinstance(direction_methods_of_fields, Iterable):
        direction_methods_of_fields = (direction_methods_of_fields,)
    return stmt.order_by(
        *(
            direction_method_of_field()
            for direction_method_of_field in direction_methods_of_fields
        )
    )


def add_offset_limit_to_query[*T](
    stmt: Select[tuple[*T]], pagination: Pagination
) -> Select[tuple[*T]]:
    if pagination.offset > 0:
        stmt = stmt.offset(pagination.offset)
    return stmt.limit(pagination.limit)


def add_order_by_and_offset_limit_to_query[M: BaseModel](
    stmt: Select[tuple[M]], order_by: dict[Any, Any], pagination: Pagination
) -> Select[tuple[M]]:
    return add_offset_limit_to_query(
        add_order_by_to_query(stmt, order_by), pagination
    )
