import aio_pika
from dishka import Provider, Scope, provide
from user_microservice.config import RabbitMQConfig



class RabbitMQProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def _get_engine(self, config: RabbitMQConfig):

