from dishka import make_async_container
from user_microservice.main.provider import MainProvider
from user_microservice.infra.postgres.provider import PostgresProvider
from user_microservice.config import Config
from user_microservice.main.config import config
from user_microservice.infra.rabbitmq.provider import RabbitMQProvider

container = make_async_container(
    MainProvider(),
    PostgresProvider(),
    RabbitMQProvider(),
    context={
        Config: config
    }
)