from sqlalchemy import select, or_
from user_microservice.application.errors import DataNotFoundError
from user_microservice.infra.postgres.gateways.base import PostgresGateway
from user_microservice.infra.postgres.tables import UserModel
from user_microservice.application.schemas.user import UserSchemas

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
