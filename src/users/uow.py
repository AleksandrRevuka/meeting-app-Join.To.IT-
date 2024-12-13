from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.adapters.uow import AsyncSqlAlchemyUnitOfWork
from src.users.repository import UsersRepository


class UsersStorageUnitOfWork(AsyncSqlAlchemyUnitOfWork):
    def __init__(self, session_factory: async_scoped_session[AsyncSession]) -> None:
        super().__init__(session_factory)

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.users = UsersRepository(session=self.session)
        return uow