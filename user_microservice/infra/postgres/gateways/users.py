from dataclasses import dataclass
from uuid import UUID
from sqlalchemy import select
from loguru import logger

from user_microservice.infra.postgres.gateways.base import PostgresGateway

from user_microservice.infra.postgres.tables import UserModel
from user_microservice.application.errors import InvalidCredentialsError
from user_microservice.application.schemas.users import UserSchemas

class GetByLoginUser(PostgresGateway):
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

        results = (await self.session.execute(stmt)).mappings().fetchone()
        logger.info(results )
        if results is None:
            raise InvalidCredentialsError()
        return UserSchemas.model_validate(results)
