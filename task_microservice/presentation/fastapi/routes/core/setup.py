from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from task_microservice.presentation.fastapi.routes.core.user.api import ROUTER as TEST_ROUTER

def setup_core_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)

    router.include_router(prefix='/user', router=TEST_ROUTER)
    return router
