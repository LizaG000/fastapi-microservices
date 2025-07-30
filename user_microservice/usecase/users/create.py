from sqlalchemy.ext.asyncio import AsyncSession
from user_microservice.usecase.base import Usecase
from user_microservice.infra.postgres.gateways.base import CreateGate
from user_microservice.application.schemas.users import CreateUserSchema
from user_microservice.infra.postgres.tables import UserModel

class CreateUserUsecase(Usecase[CreateUserSchema, None]):
    session: AsyncSession
    create_user: CreateGate[UserModel, CreateUserSchema]
    
    async def __call__(self, data: CreateUserSchema) -> None:
        async with self.session.begin():
            await self.create_user(data)
