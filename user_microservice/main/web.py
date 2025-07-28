from fastapi import FastAPI
from user_microservice.main.config import config
from user_microservice.presentation.fastapi.setup import setup_routes

app = FastAPI(
    title=config.api.project_name
)

setup_routes(app, config)
