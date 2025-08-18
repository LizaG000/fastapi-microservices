from sqlalchemy.ext.asyncio import AsyncSession
from user_microservice.usecase.base import Usecase
from user_microservice.infra.postgres.gateways.users import GetByLoginUserGate
from user_microservice.usecase.users.schemas import GetLoginUserSchemas, GetUserSchemas
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserUsecase(Usecase[GetLoginUserSchemas, GetUserSchemas]):
    session: AsyncSession
    get_user: GetByLoginUserGate
    
    async def __call__(self, data: GetLoginUserSchemas) -> GetUserSchemas:
        async with self.session.begin():
            return await self.get_user(email=data.email, password=data.password)
