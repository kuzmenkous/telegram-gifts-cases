from typing import Annotated

from fastapi import APIRouter, Depends, Response

from src.dependencies.admin import SessionToken, get_admin_by_credentials
from src.dependencies.db import Session
from src.domain.admin import AdminRead, Login
from src.models.admin import AdminModel, SessionModel
from src.services.admin import SessionService
from src.utils import set_auth_data_to_response_cookie

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login")
async def log_in(
    db_session: Session,
    admin: Annotated[AdminModel, Depends(get_admin_by_credentials)],
    response: Response,
) -> Login:
    session_model = SessionModel(admin_id=admin.id)
    db_session.add(session_model)
    await db_session.flush()
    set_auth_data_to_response_cookie(response, session_model)
    return Login(admin=AdminRead.model_validate(admin))


@auth_router.post("/logout")
async def log_out(db_session: Session, session_token: SessionToken) -> None:
    await SessionService(db_session).delete_session_by_token(session_token)
