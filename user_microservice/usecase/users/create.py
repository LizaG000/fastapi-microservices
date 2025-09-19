import aio_pika
from sqlalchemy.ext.asyncio import AsyncSession
from user_microservice.usecase.base import Usecase
from user_microservice.infra.postgres.gateways.base import CreateGate
from user_microservice.application.schemas.user import CreateUserSchema
from user_microservice.infra.postgres.tables import UserModel
from user_microservice.infra.postgres.gateways.users import  GetEmailOrPhoneGate
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, None]):
    session: AsyncSession
    create_user: CreateGate[UserModel, CreateUserSchema]
    find_user: GetEmailOrPhoneGate
    
    async def __call__(self, data: CreateUserSchema) -> None:
        async with self.session.begin():
            await self.create_user(data)
            # async with self.chanel as _chanel:
            #     await self.create_user(data)
                    # massage = aio_pika.Message(body=user.model_dump_json().encode())
                    # await _chanel.default_exchange.publish(massage, routing_key="user")
