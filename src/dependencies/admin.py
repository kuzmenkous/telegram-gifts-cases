from typing import Annotated
from uuid import UUID

from fastapi import Body, Depends, HTTPException, Response, status
from fastapi.security.api_key import APIKeyCookie
from pydantic import PositiveInt

from src.dependencies.db import Session
from src.domain.admin import AdminCredentials
from src.domain.constants.admin import SESSION_TOKEN
from src.models.admin import AdminModel, SessionModel
from src.services.admin import AdminService, SessionService
from src.utils import set_auth_data_to_response_cookie


async def get_admin_by_credentials(
    session: Session, credentials: Annotated[AdminCredentials, Body()]
) -> AdminModel:
    return await AdminService(session).get_admin_by_credentials(credentials)


async def get_session_token(
    session_token: Annotated[
        str,
        Depends(
            APIKeyCookie(
                scheme_name=SESSION_TOKEN,
                name=SESSION_TOKEN,
                description="Type: UUID",
            )
        ),
    ],
) -> UUID:
    return UUID(session_token)


SessionToken = Annotated[UUID, Depends(get_session_token)]


async def get_admin_session_by_api_token(
    db_session: Session, session_token: SessionToken, response: Response
) -> SessionModel:
    admin_session = await SessionService(db_session).get_session_by_token(
        session_token
    )
    set_auth_data_to_response_cookie(response, admin_session)
    return admin_session


AdminSession = Annotated[SessionModel, Depends(get_admin_session_by_api_token)]


async def get_admin_by_api_token(admin_session: AdminSession) -> AdminModel:
    return admin_session.admin


LoggedInAdmin = Annotated[AdminModel, Depends(get_admin_by_api_token)]


async def get_superadmin(admin: LoggedInAdmin) -> AdminModel:
    if not admin.is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmin can perform this action.",
        )
    return admin


async def get_admin_model(
    db_session: Session, admin_id: PositiveInt
) -> AdminModel:
    return await AdminService(db_session).get_admin_by_id(admin_id)
