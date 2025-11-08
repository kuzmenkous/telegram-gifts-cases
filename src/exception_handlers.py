import logging

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import ORJSONResponse, Response
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.core.schemas.errors import ServerErrorSchema
from src.core.schemas.validation import (
    ValidationErrorListSchema,
    ValidationErrorSchema,
)
from src.exceptions.http.base import BaseFieldValidationHTTPException

log = logging.getLogger(__name__)


unique_violation_sqlstate = "23505"
foreign_key_violation_sqlstate = "23503"
unique_and_foreign_key_violation_sqlstates = (
    unique_violation_sqlstate,
    foreign_key_violation_sqlstate,
)


async def field_validation_exception_handler(
    _request: Request, exc: BaseFieldValidationHTTPException
) -> ORJSONResponse:
    content = ValidationErrorSchema(field=exc.field, detail=exc.detail)
    return ORJSONResponse(
        status_code=exc.status_code,
        content=ValidationErrorListSchema(
            errors=[content.model_dump()]
        ).model_dump(),
    )


async def pydantic_validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> ORJSONResponse:
    errors = exc.errors()
    formatted_errors = []

    for error in errors:
        if error["type"] == "union_tag_not_found":
            field = ".".join(str(part) for part in error["loc"])
            detail = (
                f"Field '{field}' is missing a required discriminator "
                f"{error['ctx'].get('discriminator', 'unknown')}. "
                "Please provide this field to determine the correct type."
            )
        elif error["type"] == "json_invalid":
            field = ".".join(str(part) for part in error["loc"])
            json_error = error["ctx"].get("error", "Invalid JSON")
            detail = (
                f"Invalid JSON at '{field}'. Error: {json_error}. "
                "Please check your JSON structure and try again."
            )
        else:
            field = error["loc"][-1] if len(error["loc"]) > 0 else "unknown"
            detail = error["msg"]

        formatted_errors.append(
            ValidationErrorSchema(field=field, detail=detail).model_dump()
        )

    return ORJSONResponse(
        status_code=422,
        content=ValidationErrorListSchema(
            errors=formatted_errors
        ).model_dump(),
    )


async def http_400s_status_exception_handler(
    _request: Request, exc: HTTPException
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=exc.status_code,
        content=ServerErrorSchema(
            status_code=exc.status_code, detail=exc.detail
        ).model_dump(),
    )


async def no_result_found_exception_handler(
    _request: Request, _exc: NoResultFound
) -> Response:
    return Response(status_code=status.HTTP_404_NOT_FOUND)


async def integrity_error_exception_handler(
    _request: Request, exc: IntegrityError
) -> ORJSONResponse:
    sqlstate = exc.orig.sqlstate  # type: ignore[union-attr]
    if sqlstate in unique_and_foreign_key_violation_sqlstates:
        explanation: str = (
            exc.args[0]
            .split("DETAIL:  Key ")[-1]
            .replace("(", "")
            .replace(")", "")
        )
        status_code = status.HTTP_400_BAD_REQUEST
        if sqlstate == foreign_key_violation_sqlstate:
            status_code = status.HTTP_404_NOT_FOUND
            return ORJSONResponse(
                status_code=status_code,
                content=ServerErrorSchema(
                    status_code=status_code,
                    detail=(
                        f"{explanation.split(' is not present in table ')[0]}"
                        f" not found"
                    ),
                ),
            )
        return ORJSONResponse(
            status_code=status_code,
            content=ServerErrorSchema(
                status_code=status_code, detail=explanation
            ).model_dump(),
        )
    raise exc


def get_exception_handlers() -> dict:  # type: ignore[type-arg]
    return {
        BaseFieldValidationHTTPException: field_validation_exception_handler,
        RequestValidationError: pydantic_validation_exception_handler,
        NoResultFound: no_result_found_exception_handler,
        IntegrityError: integrity_error_exception_handler,
        status.HTTP_400_BAD_REQUEST: http_400s_status_exception_handler,
        status.HTTP_404_NOT_FOUND: http_400s_status_exception_handler,
        status.HTTP_401_UNAUTHORIZED: http_400s_status_exception_handler,
        status.HTTP_403_FORBIDDEN: http_400s_status_exception_handler,
    }
