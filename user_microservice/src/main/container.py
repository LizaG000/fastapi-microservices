from dishka import make_async_container
from user_microservice.src.main.provider import MainProvider
from user_microservice.src.infra.postgres.provider import PostgresProvider
from user_microservice.src.config import Config
from user_microservice.src.main.config import config

container = make_async_container(
    MainProvider(),
    PostgresProvider(),
    context={
        Config: config
    }
)