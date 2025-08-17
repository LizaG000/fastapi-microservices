from dishka import Provider
from dishka import Scope
from dishka import from_context
from dishka import provide
from dishka import provide_all
from fastapi import Request

from user_microservice.config import Config
from user_microservice.config import ApiConfig
from user_microservice.config import DatabaseConfig
from user_microservice.config import RabbitMQConfig

from user_microservice.usecase.users.create import CreateUserUsecase
from user_microservice.usecase.users.get_all import GetUsersUsecase
from user_microservice.usecase.users.get_user import GetUserUsecase

class MainProvider(Provider):
    scope = Scope.REQUEST

    _provide_config = from_context(provides=Config, scope=Scope.APP) 

    @provide(scope=Scope.APP)
    async def _get_api_config(self, config: Config) -> ApiConfig:
        return config.api
    
    @provide(scope=Scope.APP)
    async def _get_database_config(self, config: Config) -> DatabaseConfig:
        return config.database

    @provide(scope=Scope.APP)
    async def _get_rabbitmq_config(self, config: Config) -> RabbitMQConfig:
        return config.rabbitmq

    _request = from_context(provides=Request, scope=Scope.REQUEST)

    _get_usecases = provide_all(
        CreateUserUsecase,
        GetUsersUsecase,
        GetUserUsecase,
    )

