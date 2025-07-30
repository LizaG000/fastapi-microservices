from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from user_microservice.application.schemas.users import CreateUserSchema
from user_microservice.usecase.users.create import CreateUserUsecase

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_users() -> str:
    return "УРАААААА"

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_users(
    usecase: FromDishka[CreateUserUsecase],
    user: CreateUserSchema) -> None:
    await usecase(user)
