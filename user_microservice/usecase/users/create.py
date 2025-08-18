import aio_pika
import json
from sqlalchemy.ext.asyncio import AsyncSession
from user_microservice.usecase.base import Usecase
from user_microservice.infra.postgres.gateways.base import CreateReturningGate
from user_microservice.application.schemas.user import CreateUserSchema
from user_microservice.infra.postgres.tables import UserModel
from aio_pika.abc import AbstractChannel
from user_microservice.infra.postgres.gateways.users import  GetEmailOrPhoneGate
from user_microservice.application.errors import DataNotFoundError, ConflictPhoneError, ConflictEmailError
from user_microservice.usecase.users.schemas import GetUserSchemas
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, GetUserSchemas]):
    session: AsyncSession
    chanel: AbstractChannel
    create_user: CreateReturningGate[UserModel, CreateUserSchema, GetUserSchemas]
    find_user: GetEmailOrPhoneGate
    
    async def __call__(self, data: CreateUserSchema) -> GetUserSchemas:
        async with self.session.begin():
            try:
                user = await self.find_user(data.email, data.phone)
                if user.email == data.email:
                    raise  ConflictEmailError()
                raise ConflictPhoneError()
            except DataNotFoundError:
                async with self.chanel as _chanel:
                    user = await self.create_user(data)
                    massage = aio_pika.Message(body=user.model_dump_json().encode())
                    await _chanel.default_exchange.publish(massage, routing_key="user")
                    return user
