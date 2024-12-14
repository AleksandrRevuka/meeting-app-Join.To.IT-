from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.events.repository import EventsRegistrationRepository, EventsRepository
from src.adapters.uow import AsyncSqlAlchemyUnitOfWork


class EventsStorageUnitOfWork(AsyncSqlAlchemyUnitOfWork):
    def __init__(self, session_factory: async_scoped_session[AsyncSession]) -> None:
        super().__init__(session_factory)

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.events = EventsRepository(session=self.session)
        self.registrations = EventsRegistrationRepository(session=self.session)
        return uow