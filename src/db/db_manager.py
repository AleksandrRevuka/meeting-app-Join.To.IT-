from asyncio import current_task
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import click
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.config import database_config as db_config
from src.orm import SqlAlchemyBase


class AsyncDatabaseSQLAlchemyManager:
    def __init__(self, db_uri: str) -> None:
        self._db_uri = db_uri
        self._engine: AsyncEngine | None = None
        self._session_factory: async_scoped_session[AsyncSession] | None = None

    async def create_database(self) -> None:
        assert self._engine is not None
        async with self._engine.begin() as conn:
            await conn.run_sync(SqlAlchemyBase.metadata.create_all)

    async def connect(self, **kwargs: Any) -> None:
        self._engine = create_async_engine(self._db_uri, **kwargs)

    async def disconnect(self) -> None:
        assert self._engine is not None
        await self._engine.dispose()

    def init_session_factory(self) -> None:
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=db_config.DATABASE_AUTO_COMMIT,
                autoflush=db_config.DATABASE_AUTO_FLUSH,
                expire_on_commit=db_config.DATABASE_EXPIRE_ON_COMMIT,
                bind=self._engine,
            ),
            scopefunc=current_task,
        )

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        assert self._session_factory is not None

        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception as err:
            click.secho(f"ERROR:    {err}", fg="bright_red")
            await session.rollback()
            raise
        finally:
            await session.close()

    async def get_db_session(self) -> AsyncIterator[AsyncSession]:
        assert self._session_factory is not None

        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception as err:
            click.secho(f"ERROR:    {err}", fg="bright_red")
            await session.rollback()
            raise
        finally:
            await session.close()

    @property
    def engine(self) -> AsyncEngine:
        assert self._engine is not None
        return self._engine

    @property
    def session_factory(self) -> async_scoped_session[AsyncSession]:
        assert self._session_factory is not None
        return self._session_factory
