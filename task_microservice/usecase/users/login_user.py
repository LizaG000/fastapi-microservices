from sqlalchemy.ext.asyncio import AsyncSession
from task_microservice.usecase.base import Usecase
from task_microservice.infra.postgres.gateways.base import CreateReturningGate
from task_microservice.application.schemas.user import CreateUserSchema
from task_microservice.infra.postgres.tables import UserModel
from task_microservice.application.schemas.user import UserSchemas
from dataclasses import dataclass

from user_microservice.presentation.fastapi.routes.core.users.api import create_users


@dataclass(slots=True, frozen=True, kw_only=True)
class LoginUserUsecase(Usecase[CreateUserSchema, UserSchemas]):
    session: AsyncSession
    create_user: CreateReturningGate[UserModel, CreateUserSchema, UserSchemas]
    
    async def __call__(self, data: CreateUserSchema) -> UserSchemas:
        async with self.session.begin():
            return await self.create_user(data)
