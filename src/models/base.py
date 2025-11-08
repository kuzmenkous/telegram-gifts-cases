import enum
from datetime import datetime
from typing import Annotated, Any, ClassVar

from sqlalchemy import (
    DateTime,
    Enum,
    Identity,
    Integer,
    MetaData,
    func,
    inspect,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData(
    naming_convention={
        # Index naming
        "ix": "ix__%(table_name)s__%(column_0_N_name)s",
        # Unique constraint naming
        "uq": "uq__%(table_name)s__%(column_0_N_name)s",
        # Check constraint naming
        "ck": "ck__%(table_name)s__%(constraint_name)s",
        # Foreign key naming
        "fk": (
            "fk__%(table_name)s__%(column_0_N_name)s__%(referred_table_name)s"
        ),
        # Primary key naming
        "pk": "pk__%(table_name)s",
    }
)

Id = Annotated[
    int, mapped_column(Integer, Identity(), primary_key=True, sort_order=-1)
]


class BaseModel(AsyncAttrs, DeclarativeBase):
    id: Mapped[Id]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), sort_order=100
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), sort_order=100
    )

    metadata = metadata

    type_annotation_map: ClassVar[dict[Any, Any]] = {
        dict[str, Any]: JSONB,
        dict[str, str]: JSONB,
        datetime: DateTime(timezone=True),
        enum.Enum: Enum(enum.Enum, inherit_schema=True),
    }

    def __setattr__(self, key: str, value: object) -> None:
        if (value_is_dict := isinstance(value, dict)) or (
            value_is_list_of_dicts := (
                isinstance(value, list)
                and all(isinstance(item, dict) for item in value)
            )
        ):
            relationship = inspect(self).mapper.relationships.get(key)
            if relationship is not None:
                try:
                    if value_is_dict:
                        if not relationship.uselist:
                            value = relationship.mapper.class_(**value)
                    elif value_is_list_of_dicts:  # noqa: SIM102
                        if relationship.uselist:
                            value = [
                                relationship.mapper.class_(**item)
                                for item in value
                            ]
                except TypeError:
                    pass
        super().__setattr__(key, value)

    def setattr_for_update_with_nested_relationships(
        self, field_name: str, field_value: object
    ) -> None:
        if (
            isinstance(field_value, dict)
            and field_name in inspect(self).mapper.relationships
        ):
            nested_model = getattr(self, field_name)
            for nested_field_name, nested_value in field_value.items():
                nested_model.setattr_for_update_with_nested_relationships(
                    nested_field_name, nested_value
                )
        else:
            setattr(self, field_name, field_value)

    def __repr__(self) -> str:
        return self.__str__()
