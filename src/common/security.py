from datetime import UTC, datetime, timedelta

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.container import Container
from src.config.base_config import settings
from src.users.uow import UsersStorageUnitOfWork
from src.users.exceptions import user_exceptions as user_err
from src.users.schemas import PrivateUser


class SecurityService:
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    async def create_access_token(
        self, data: dict[str, str | datetime], expires_delta: float | None = None
    ) -> str:
        """
        The create_access_token function creates a new access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(UTC) + timedelta(minutes=60)
        to_encode.update({"iat": datetime.now(UTC), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return str(encoded_access_token)

    @inject
    async def get_current_user(
        self,
        uow: UsersStorageUnitOfWork = Depends(Provide[Container.users_storege_unit_of_work]),
        token: str = Depends(oauth2_scheme),
    ) -> PrivateUser:
        """
        The get_current_user function is a dependency that will be used in the
        protected endpoints. It takes a token as an argument and returns the user
        if it's valid, otherwise raises an HTTPException with status code 401.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception from e

        async with uow:
            user = await uow.users.get_one(email=email)
            if user is None:
                raise user_err.UserNotFoundError()

        return user


security_service = SecurityService()
