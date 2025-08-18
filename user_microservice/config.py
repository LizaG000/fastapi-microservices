import os
from pydantic import ConfigDict
from dynaconf import Dynaconf
from loguru import logger

from user_microservice.application.schemas.common import BaseSchema


class ApiConfig(BaseSchema):
    host: str = 'localhost'
    port: int = 8000
    project_name: str = 'base'

class DatabaseConfig(BaseSchema):
    host: str = os.getenv('HOST')
    port: int = os.getenv('PORT')
    username: str = os.getenv('POSTGRES_USER')
    password: str = os.getenv('POSTGRES_PASSWORD')
    database: str = os.getenv('POSTGRES_DB')
    driver: str = 'postgresql+psycopg_async'

    @property
    def dsn(self,) -> str:
        return f'{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'

class RabbitMQConfig(BaseSchema):
    user: str = 'rabbitmq'
    password: str = 'rabbitmq'
    vhost: str = '/'
    host: str = 'rabbitmq'
    port: int = 5672


class Config(BaseSchema):
    model_config = ConfigDict(extra='allow', from_attributes=True)
    api: ApiConfig
    database: DatabaseConfig
    rabbitmq: RabbitMQConfig


def get_config() -> Config:
    dynaconf = Dynaconf(
        settings_files=[
            '././deploy/configs/config_user_microservice.toml'
        ],
        envvar_prefix='Liza',
        load_dotenv=True,
    )
    logger.info(dynaconf.api)
    return Config.model_validate(dynaconf)