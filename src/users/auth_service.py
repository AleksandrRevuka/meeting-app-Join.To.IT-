from src.users.uow import UsersStorageUnitOfWork
from src.users.schemas import PrivateUser, TokenModel, UserCreate
from src.users.exceptions import auth_exceptions as auth_err
from src.users.exceptions import user_exceptions as user_err
from src.users.utils import verify_password


class AuthUsersService:
    def __init__(self, uow: UsersStorageUnitOfWork):
        self.uow = uow

    async def create_user(
        self,
        body: UserCreate,
    ) -> PrivateUser:
        async with self.uow:
            if await self.uow.users.get_one(email=body.email):
                raise user_err.UserWithEmailAlreadyExistsError()
            elif await self.uow.users.get_one(phone=body.phone):
                raise user_err.UserWithPhoneAlreadyExistsError()

            new_user: PrivateUser = await self.uow.users.add_one(body)
            await self.uow.commit()

            return new_user

    async def user_login(self, email: str, password: str) -> TokenModel:
        from src.common.security import security_service
        async with self.uow:
            user: PrivateUser = await self.uow.users.get_one(email=email)
            if user is None:
                raise auth_err.UserNotFoundUnAuthorizedError()
            elif not verify_password(password, user.password):
                raise auth_err.InvalidPasswordError()

            access_token = await security_service.create_access_token(
                data={"sub": user.email}
            )

            return TokenModel(access_token=access_token)