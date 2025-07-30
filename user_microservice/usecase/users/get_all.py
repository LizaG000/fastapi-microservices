from sqlalchemy.ext.asyncio import AsyncSession
from user_microservice.usecase.base import Usecase
from user_microservice.infra.postgres.gateways.base import GetAllGate
from user_microservice.application.schemas.users import UserSchemas
from user_microservice.infra.postgres.tables import UserModel

class GetUsersUsecase(Usecase[None, None]):
    session: AsyncSession
    get_users: GetAllGate[UserModel, UserSchemas]
    
    async def __call__(self) -> None:
        async with self.session.begin():
            await self.get_users()
