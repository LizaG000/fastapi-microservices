from sqlalchemy.ext.asyncio import AsyncSession
from user_microservice.usecase.base import Usecase
from user_microservice.infra.postgres.gateways.users import GetByLoginUser
from user_microservice.application.schemas.users import UserSchemas
from user_microservice.usecase.users.schemas import GetLoginUserSchemas
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserUsecase(Usecase[GetLoginUserSchemas, UserSchemas]):
    session: AsyncSession
    get_user: GetByLoginUser
    
    async def __call__(self, data: GetLoginUserSchemas) -> UserSchemas:
        async with self.session.begin():
            return await self.get_user(email=data.email, password=data.password)
