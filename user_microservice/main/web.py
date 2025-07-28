from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from user_microservice.main.config import config
from user_microservice.presentation.fastapi.setup import setup_routes
from user_microservice.main.container import container

app = FastAPI(
    title=config.api.project_name
)

setup_routes(app, config)
setup_dishka(container, app)
