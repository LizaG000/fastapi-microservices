from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Query
from fastapi import status
from user_microservice.application.schemas.user import CreateUserSchema
from user_microservice.usecase.users.create import CreateUserUsecase

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_users(
    usecase: FromDishka[CreateUserUsecase],
    user: CreateUserSchema) -> None:
    return await usecase(user)

