from dataclasses import dataclass
from aio_pika.abc import AbstractConnection, AbstractQueue
from collections.abc import AsyncIterator
from dishka import Provider, provide,Scope
from loguru import logger

@dataclass(slots=True, kw_only=True)
class ChanelProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    async def _get_chanel_1_(self, connection: AbstractConnection) -> AsyncIterator[AbstractQueue]:
        chanel: AbstractQueue | None = None
        async with connection as connect:
            try:
                if chanel is None:
                    chanel = await connect.channel().declare_queue("", durable=True)
                yield chanel
            except Exception as e:
                logger.error('Error connection to chanel 1', e)
            finally:
                await chanel.close()
