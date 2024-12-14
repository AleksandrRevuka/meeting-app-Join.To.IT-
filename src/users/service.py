import uuid
from src.users.uow import UsersStorageUnitOfWork
from src.users.schemas import PrivateUser, UserUpdate
from src.users.exceptions import user_exceptions as user_err


class UsersService:
    def __init__(self, uow: UsersStorageUnitOfWork):
        self.uow = uow

    async def get_user_by_id(self, user_id: uuid.UUID) -> PrivateUser:
        async with self.uow:
            user: PrivateUser | None = await self.uow.users.get_one(user_id=user_id)
            if user is None:
                raise user_err.UserNotFoundError()
            return user
        
    async def update_user(self, user_id: uuid.UUID, body: UserUpdate) -> PrivateUser:
        async with self.uow:
            user: PrivateUser | None = await self.uow.users.get_one(user_id=user_id)
            if user is None:
                raise user_err.UserNotFoundError()
            updated_user = await self.uow.users.update_one(body, user_id=user_id)
            await self.uow.commit()
        return updated_user
        
    async def delete_user(self, user_id: uuid.UUID) -> None:
        async with self.uow:
            user: PrivateUser | None = await self.uow.users.get_one(user_id=user_id)

            if user is None:
                raise user_err.UserNotFoundError()
            await self.uow.users.delete_one(user_id=user.user_id)

            await self.uow.commit()