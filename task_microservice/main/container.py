from dishka import make_async_container
from task_microservice.main.provider import MainProvider
from task_microservice.infra.postgres.provider import PostgresProvider
from task_microservice.config import Config
from task_microservice.main.config import config

container = make_async_container(
    MainProvider(),
    PostgresProvider(),
    context={
        Config: config
    }
)