from fastapi import FastAPI
from task_microserver.main.config import config
from task_microserver.presentation.fastapi.setup import setup_routes

app = FastAPI(
    title=config.api.project_name
)

setup_routes(app, config)
