from typing import Any, Protocol, Self
import traceback as tb
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

import logging

logger = logging.getLogger("uvicorn")


class AsyncBaseUnitOfWork(Protocol):
    def __init__(self) -> None: ...

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: Any) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class AsyncSqlAlchemyUnitOfWork(AsyncBaseUnitOfWork):
    def __init__(self, session_factory: async_scoped_session[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    @property
    def session(self) -> AsyncSession:
        assert self._session is not None
        return self._session

    async def __aenter__(self) -> Self:
        """
        Entering the SqlAlchemyUnitOfWork.
        """
        self._session = self._session_factory()
        logger.info(f"Open session UOW: {self.session.__str__()}")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Exiting the SqlAlchemyUnitOfWork.
        """
        if exc_type:
            logger.error(
                f"An error occurred: {exc_type.__name__}: {exc_value}\n"
                f"Traceback:\n{''.join(tb.format_tb(traceback))}"
            )
            await self.rollback()
        logger.info(f"Close session UOW: {self.session.__str__()}")

        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        self.session.expunge_all()
        await self.session.rollback()
