from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound

from src.constants.admin import password_hasher
from src.models.admin import AdminModel, SessionModel
from src.repositories.admin import AdminRepository, SessionRepository
from src.schemas.admin import AdminCreate, AdminCredentials
from src.services.base import BaseService


class AdminService(BaseService):
    async def get_admin_by_credentials(
        self, credentials: AdminCredentials
    ) -> AdminModel:
        try:
            admin = await AdminRepository().get_admin_by_username(
                self._session, credentials.username
            )
            password_hasher.verify(
                admin.hashed_password, credentials.password.get_secret_value()
            )
        except (NoResultFound, VerifyMismatchError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        if password_hasher.check_needs_rehash(admin.hashed_password):
            admin.hashed_password = password_hasher.hash(
                credentials.password.get_secret_value()
            )
            self._session.add(admin)
            await self._session.commit()
        return admin

    async def get_admin_by_id(self, admin_id: int) -> AdminModel:
        return await AdminRepository().get_admin(self._session, admin_id)

    async def create_admin(self, admin_create: AdminCreate) -> int:
        admin_model = AdminModel(
            username=admin_create.username,
            hashed_password=admin_create.hashed_password,
        )
        self._session.add(admin_model)
        await self._session.flush()

        return admin_model.id

    async def delete_admin(self, admin_id: int) -> None:
        await AdminRepository().delete_admin(self._session, admin_id)


class SessionService(BaseService):
    async def get_session_by_token(self, token: UUID) -> SessionModel:
        admin_session = await SessionRepository().get_session_by_token(
            self._session, token
        )
        if not admin_session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return admin_session

    async def delete_session_by_token(self, token: UUID) -> None:
        await SessionRepository().delete_session_by_token(self._session, token)
