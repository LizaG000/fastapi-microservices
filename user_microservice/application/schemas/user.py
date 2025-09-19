from uuid import UUID
from datetime import datetime
from user_microservice.application.schemas.common import BaseSchema

class UserSchemas(BaseSchema):
    id: UUID
    login: str
    password: str
    created_at: datetime
    updated_at: datetime

class CreateUserSchema(BaseSchema):
    login: str
    password: str
