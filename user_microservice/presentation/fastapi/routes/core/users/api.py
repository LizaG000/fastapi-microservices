from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Query
from fastapi import status
from user_microservice.application.schemas.user import CreateUserSchema, UserSchemas
from user_microservice.usecase.users.create import CreateUserUsecase
from user_microservice.usecase.users.get_all import GetUsersUsecase
from user_microservice.usecase.users.get_user import GetUserUsecase
from user_microservice.usecase.users.schemas import GetLoginUserSchemas
from user_microservice.usecase.users.schemas import GetUserSchemas

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_users(usecase: FromDishka[GetUsersUsecase]) -> list[UserSchemas]:
    return await usecase()

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_users(
    usecase: FromDishka[CreateUserUsecase],
    user: CreateUserSchema) -> GetUserSchemas:
    return await usecase(user)

@ROUTER.get('/login', status_code=status.HTTP_200_OK)
async def get_user(
    usecase: FromDishka[GetUserUsecase],
    data: GetLoginUserSchemas = Query(),
    ) -> GetUserSchemas:
    return await usecase(data=data)
