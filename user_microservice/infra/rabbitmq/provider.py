import aio_pika
from dishka import Provider, Scope, provide, provide_all
from aio_pika import connect
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue
from collections.abc import AsyncIterator
from user_microservice.config import RabbitMQConfig
from loguru import logger


class RabbitMQProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    async def _get_engine(self, config: RabbitMQConfig) -> AsyncIterator[AbstractConnection]:
        connection: AbstractConnection | None = None
        try:
            if connection is None:
                connection = await connect(
                    host=config.host,
                    port=config.port,
                    login=config.user,
                    password=config.password,
                    virtualhost=config.vhost
                     )
            yield connection
        except ConnectionRefusedError as e:
            logger.error('Error connecting to RabbitMQ', e)
        finally:
            if connection is not None:
                await connection.close()

    @provide(scope=Scope.APP)
    async def _get_chanel_1_(self, connection: AbstractConnection) -> AsyncIterator[AbstractChannel]:
        chanel: AbstractChannel | None = None
        async with connection as _connection:
            try:
                if chanel is None:
                    chanel = await _connection.channel()
                yield chanel
            except Exception as e:
                logger.error('Error connection to chanel 1', e)
            finally:
                await chanel.close()

    @provide(scope=Scope.APP)
    async def _get_queue_1_(self, chanel: AbstractChannel) -> AsyncIterator[AbstractQueue]:
        queue: AbstractQueue | None = None
        async with chanel as _chanel:
            try:
                if queue is None:
                    queue = await _chanel.declare_queue("user", durable=True)
                yield queue
            except Exception as e:
                logger.error('Error connection to qeue 1', e)
            finally:
                await queue.cancel("user")
