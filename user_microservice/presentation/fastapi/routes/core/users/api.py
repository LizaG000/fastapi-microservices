from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from user_microservice.infra.postgres.gateways.base import GetAllGate, CreateGate
from user_microservice.application.schemas.users import CreateUserSchema
from user_microservice.infra.postgres.tables import UserModel
from sqlalchemy.ext.asyncio import AsyncSession

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_users() -> str:
    return "УРАААААА"

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_users(
    session: FromDishka[AsyncSession],
    create_gate: FromDishka[CreateGate[UserModel, CreateUserSchema]],
    user: CreateUserSchema) -> None:
    async with session.begin():
        await create_gate(user)
