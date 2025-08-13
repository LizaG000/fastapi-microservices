from dataclasses import dataclass
from uuid import UUID
from sqlalchemy import select, or_
from loguru import logger
from user_microservice.application.errors import DataNotFoundError
from user_microservice.infra.postgres.gateways.base import PostgresGateway
from user_microservice.infra.postgres.tables import UserModel
from user_microservice.application.errors import InvalidCredentialsError
from user_microservice.application.schemas.users import UserSchemas

class GetByLoginUserGate(PostgresGateway):
    async def __call__(self, email: str, password: str):
        stmt = (select(
            UserModel.id,
            UserModel.name,
            UserModel.age,
            UserModel.phone,
            UserModel.email,
            UserModel.created_at,
            UserModel.updated_at
        ).where(
            UserModel.email == email,
            UserModel.password == password
        ))
        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise InvalidCredentialsError()
        return UserSchemas.model_validate(result)

class GetEmailOrPhoneGate(PostgresGateway):
    async def __call__(self, email: str, phone: int):
        stmt = (select(
            UserModel.__table__.columns
        ).where(or_(
            UserModel.email == email,
            UserModel.phone == phone
        )))
        result = (await self.session.execute(stmt)).mappings().first()
        if result is None:
            raise DataNotFoundError(UserModel)
        return UserSchemas.model_validate(result)
