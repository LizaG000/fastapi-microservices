from fastapi import Query
from user_microservice.application.schemas.common import BaseModel

class GetLoginUserSchemas(BaseModel):
    email: str = Query()
    password: str = Query()

