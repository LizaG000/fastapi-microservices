from dataclasses import dataclass
from sqlalchemy import select, insert
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from sqlalchemy.sql.dml import ReturningInsert
from sqlalchemy.sql.dml import ReturningUpdate
from user_microservice.application.errors import DataNotFoundError

from user_microservice.infra.postgres.tables import BaseDBModel

TAppliable = Select | ReturningInsert | ReturningUpdate

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetAllGate[TTable: BaseDBModel, TEntity: BaseModel](
    PostgresGateway,
):
    table: type[TTable]
    schema_type: type[TEntity]

    async def __call__(self,) -> list[TEntity]:
        stmt = select(*self.table.group_by_fields())
        results = (await self.session.execute(stmt)).mappings().fetchall()
        if len(results) == 0:
            raise DataNotFoundError(self.table)
        return [self.schema_type.model_validate(result) for result in results]

@dataclass(slots=True, kw_only=True)
class CreateGate[TTable: BaseDBModel, TCreate: BaseModel](
    PostgresGateway,
):
    table: type[TTable]
    create_schema_type: type[TCreate]

    async def __call__(self, entity: TCreate) -> None:
        stmt = insert(self.table).values(**entity.model_dump())
        await self.session.execute(stmt)

@dataclass(slots=True, kw_only=True)
class CreateReturningGate[TTable: BaseDBModel, TCreate: BaseModel, TSchema: BaseModel](
    PostgresGateway,
):
    table: type[TTable]
    create_schema_type: type[TCreate]
    return_schema_type: type[TSchema]

    async def __call__(self, entity: TCreate) -> TSchema:
        stmt = insert(self.table).values(**entity.model_dump()).returning(self.table.__table__.columns)
        result = (await self.session.execute(stmt)).mappings().first()
        return self.return_schema_type.model_validate(result)