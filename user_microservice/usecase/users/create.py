from sqlalchemy.ext.asyncio import AsyncSession
from user_microservice.usecase.base import Usecase
from user_microservice.infra.postgres.gateways.base import CreateReturningGate
from user_microservice.application.schemas.user import CreateUserSchema
from user_microservice.infra.postgres.tables import UserModel
from user_microservice.application.schemas.user import UserSchemas
from user_microservice.infra.postgres.gateways.users import  GetEmailOrPhoneGate
from user_microservice.application.errors import DataNotFoundError, ConflictPhoneError, ConflictEmailError
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, UserSchemas]):
    session: AsyncSession
    create_user: CreateReturningGate[UserModel, CreateUserSchema, UserSchemas]
    find_user: GetEmailOrPhoneGate
    
    async def __call__(self, data: CreateUserSchema) -> UserSchemas:
        async with self.session.begin():
            try:
                user = await self.find_user(data.email, data.phone)
                if user.email == data.email:
                    raise  ConflictEmailError()
                raise ConflictPhoneError()
            except DataNotFoundError:
                return await self.create_user(data)
