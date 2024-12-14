from abc import ABC, abstractmethod
from typing import Any, Generic

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import TypeVar

from src.adapters.orm import SqlAlchemyBase


ModelType = TypeVar("ModelType", bound=SqlAlchemyBase)

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class IRepository(ABC):
    """
    Abstract base repository interface for basic CRUD operations.
    """

    @abstractmethod
    async def get_all(
        self,
        schema_override: Any | None,
        **filter_by: Any,
    ) -> list[Any]: ...

    @abstractmethod
    async def add_one(
        self, data: BaseModel | dict[str, Any], schema_override: Any | None = None
    ) -> Any: ...

    @abstractmethod
    async def get_one(
        self,
        relationships: Any = None,
        schema_override: Any | None = None,
        **filter_by: Any,
    ) -> Any: ...

    @abstractmethod
    async def update_one(
        self,
        data: BaseModel | dict[str, Any],
        schema_override: Any | None,
        **filter_by: Any,
    ) -> Any: ...

    @abstractmethod
    async def delete_one(
        self,
        **filter_by: Any,
    ) -> None: ...


class AsyncRepository(Generic[ModelType, SchemaType]):
    """
    Repository implementation for SQLAlchemy models and Pydantic schemas.
    """

    model: type[ModelType]
    schema: type[SchemaType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        schema_override: type[SchemaType] | None = None,
        **filter_by: Any,
    ) -> list[SchemaType]:
        """
        Fetch all entities and validate them against the specified schema.
        :param schema_override: Optional Pydantic schema to override the default.
        """
        schema = schema_override or self.schema
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        entities = result.scalars().all()
        return [schema.model_validate(entity.__dict__) for entity in entities]

    async def add_one(
        self,
        data: BaseModel | dict[str, Any],
        schema_override: type[SchemaType] | None = None,
    ) -> SchemaType:
        """
        Add a new entity to the database. Accepts Pydantic model or dict as input.
        :param data: Pydantic model or dictionary containing data for the new entity.
        :param schema_override: Optional Pydantic schema for validation after insertion.
        """
        schema = schema_override or self.schema
        data = data if isinstance(data, dict) else data.model_dump()

        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        entity = result.scalar_one()
        return schema.model_validate(entity.__dict__)

    async def update_one(
        self,
        data: BaseModel | dict[str, Any],
        schema_override: type[SchemaType] | None = None,
        **filter_by: Any,
    ) -> SchemaType:
        """
        Update an entity based on filter criteria.
        :param data: Pydantic model or dictionary containing updated data.
        :param schema_override: Optional Pydantic schema for validation after update.
        """
        schema = schema_override or self.schema
        data = data if isinstance(data, dict) else data.model_dump()

        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(**filter_by)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        entity = result.scalar_one()
        return schema.model_validate(entity.__dict__)

    async def delete_one(
        self,
        **filter_by: Any,
    ) -> None:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        await self.session.execute(stmt)

    async def get_one(self, **filter_by: Any) -> SchemaType | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        entity = result.scalar_one_or_none()
        return self.schema.model_validate(entity.__dict__) if entity else None
