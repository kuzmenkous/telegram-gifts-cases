import time

from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data
from fastapi import Body, HTTPException, status

from src.core.config import settings


async def get_verified_and_parsed_init_data(
    init_data: str = Body(..., media_type="text/plain")
) -> WebAppInitData:
    try:
        parsed_data = safe_parse_webapp_init_data(
            settings.telegram.bot_token, init_data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid init data signature",
        ) from e

    current_timestamp = int(time.time())
    auth_timestamp = int(parsed_data.auth_date.timestamp())
    age_seconds = current_timestamp - auth_timestamp

    if age_seconds > settings.telegram.init_data_expire:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Init data has expired",
        )

    return parsed_data
