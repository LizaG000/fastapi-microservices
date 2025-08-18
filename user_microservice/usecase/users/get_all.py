from sqlalchemy.ext.asyncio import AsyncSession
from user_microservice.usecase.base import Usecase
from user_microservice.infra.postgres.gateways.base import GetAllGate
from user_microservice.application.schemas.user import UserSchemas
from user_microservice.infra.postgres.tables import UserModel
from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class GetUsersUsecase(Usecase[None, list[UserSchemas]]):
    session: AsyncSession
    get_users: GetAllGate[UserModel, UserSchemas]

    async def __call__(self, ) -> list[UserSchemas]:
        async with self.session.begin():
            return await self.get_users()
