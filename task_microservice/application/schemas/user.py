from uuid import UUID
from datetime import datetime
from task_microservice.application.schemas.common import BaseModel

class UserSchemas(BaseModel):
    id: UUID
    name: str
    age: int
    created_at: datetime
    updated_at: datetime

class CreateUserSchema(BaseModel):
    name: str
    age: int
