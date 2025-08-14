from sqlalchemy import select, or_
from user_microservice.application.errors import DataNotFoundError
from user_microservice.infra.postgres.gateways.base import PostgresGateway
from user_microservice.infra.postgres.tables import UserModel
from user_microservice.application.errors import InvalidCredentialsError
from user_microservice.application.schemas.user import UserSchemas
from user_microservice.usecase.users.schemas import GetUserSchemas

class GetByLoginUserGate(PostgresGateway):
    async def __call__(self, email: str, password: str) -> GetUserSchemas:
        stmt = (select(
            UserModel.id,
            UserModel.name,
            UserModel.age,
        ).where(
            UserModel.email == email,
            UserModel.password == password
        ))
        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise InvalidCredentialsError()
        return GetUserSchemas.model_validate(result)

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
