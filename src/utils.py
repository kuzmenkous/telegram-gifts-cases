from fastapi import Response

from src.domain.constants.admin import SESSION_TOKEN
from src.models.admin import SessionModel


def set_auth_data_to_response_cookie(
    response: Response, admin_session: SessionModel
) -> None:
    response.set_cookie(key=SESSION_TOKEN, value=str(admin_session.token))
