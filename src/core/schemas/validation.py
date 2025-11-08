from pydantic import BaseModel


class ValidationErrorSchema(BaseModel):
    field: str
    detail: str


class ValidationErrorListSchema(BaseModel):
    errors: list[ValidationErrorSchema]
