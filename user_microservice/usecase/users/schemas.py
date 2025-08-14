from fastapi import Query
from user_microservice.application.schemas.common import BaseModel
from uuid import UUID

class GetLoginUserSchemas(BaseModel):
    email: str = Query()
    password: str = Query()

class GetUserSchemas(BaseModel):
    id: UUID
    name: str
    age: int
    phone: int
    email: str
