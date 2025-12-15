from dataclasses import dataclass
from functools import cached_property
from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    Field,
    SecretStr,
    computed_field,
    model_validator,
)

from src.domain.base import CreatedAtMixin, IdSchema, OrderByBase
from src.domain.constants.admin import password_hasher

Password = Annotated[SecretStr, Field(min_length=6)]
_PasswordForCheck = Annotated[Password, Field(exclude=True)]


class UsernameMixin(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class AdminBase(UsernameMixin, BaseModel):
    pass


class AdminCreate(AdminBase):
    password: _PasswordForCheck
    password2: _PasswordForCheck

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if (
            self.password.get_secret_value()
            != self.password2.get_secret_value()
        ):
            raise ValueError("Passwords don't match")
        return self

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def hashed_password(self) -> str:
        return password_hasher.hash(self.password.get_secret_value())


class AdminUpdate(UsernameMixin, BaseModel):
    is_superadmin: bool


class AdminRead(CreatedAtMixin, AdminUpdate, AdminBase, IdSchema):
    pass


class AdminCredentials(BaseModel):
    username: str
    password: _PasswordForCheck


class Login(BaseModel):
    status: Literal["ok"] = "ok"
    admin: AdminRead


@dataclass
class AdminFilters:
    username__ilike: str | None = None
    is_superadmin: bool | None = None


type OrderBy = OrderByBase[Literal["username", "is_superadmin", "created_at"]]
