from functools import cached_property
from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    Field,
    SecretStr,
    computed_field,
    model_validator,
)

from src.constants.admin import password_hasher
from src.schemas.base import CreatedAtMixin, IdSchema

Password = Annotated[SecretStr, Field(min_length=6)]
_PasswordForCheck = Annotated[Password, Field(exclude=True)]


class AdminBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)


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


class AdminRead(CreatedAtMixin, AdminBase, IdSchema):
    pass


class AdminCredentials(BaseModel):
    username: str
    password: _PasswordForCheck


class Login(BaseModel):
    status: Literal["ok"] = "ok"
    user: AdminRead
