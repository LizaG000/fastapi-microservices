from dishka import make_async_container
from task_microserver.main.provider import MainProvider
from task_microserver.infra.postgres.provider import PostgresProvider
from task_microserver.config import Config
from task_microserver.main.config import config

container = make_async_container(
    MainProvider(),
    PostgresProvider(),
    context={
        Config: config
    }
)