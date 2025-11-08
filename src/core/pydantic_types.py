from typing import Annotated, Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class _ZoneInfoPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> ZoneInfo:
            try:
                return ZoneInfo(value)
            except ZoneInfoNotFoundError:
                raise ValueError("Invalid timezone")

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(
                    validate_from_str
                ),
            ]
        )
        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first
                    # before doing any further work
                    core_schema.is_instance_schema(ZoneInfo),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance), when_used="json"
            ),
        )


TimezoneInfo = Annotated[ZoneInfo, _ZoneInfoPydanticAnnotation]
