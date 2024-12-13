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
    SECRET_KEY = settings.secret_key  # .jwt_secret_key
    ALGORITHM = settings.algorithm  # jwt_algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    async def create_access_token(
        self, data: dict[str, str | datetime], expires_delta: float | None = None
    ) -> str:
        """
        The create_access_token function creates a new access token.

        :param data: dict: Pass the data that will be encoded in the access token
        :param expires_delta: Optional[float]: Set the expiration time of the token
        :return: An encoded access token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(UTC) + timedelta(minutes=60)
        to_encode.update({"iat": datetime.now(UTC), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return str(encoded_access_token)

    async def create_refresh_token(
        self, data: dict[str, str | datetime], expires_delta: float | None = None
    ) -> str:
        """
        The create_refresh_token function creates a refresh token for the user.

        :param data: dict: Pass in the user's information, such as their username and email
        :param expires_delta: Optional[float]: Set the expiry time of the refresh token
        :return: An encoded token that contains the data passed to it as well as a timestamp
        when the token was created and an expiration date
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(UTC) + timedelta(hours=12)
        to_encode.update({"iat": datetime.now(UTC), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return str(encoded_refresh_token)

    async def decode_refresh_token(self, refresh_token: str) -> str:
        """
        The decode_refresh_token function is used to decode the refresh token.
        It takes a refresh_token as an argument and returns the email of the user if it's valid.
        If not, it raises an HTTPException with status code 401 (UNAUTHORIZED)
        and detail 'Could not validate credentials'.

        :param refresh_token: str: Pass the refresh token to the function
        :return: The email of the user associated with the refresh token
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return str(email)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            ) from e

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

        :param token: str: Get the token from the authorization header
        :param db: Session: Pass the database session to the function
        :return: A user object or None
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Decode JWT
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

    def create_email_token(self, data: dict[str, str | datetime]) -> str:
        """
        The create_email_token function takes a dictionary of data and returns a token.
        The token is created by encoding the data with the SECRET_KEY and ALGORITHM,
        and adding an iat (issued at) timestamp and exp (expiration) timestamp to it.

        :param data: dict: Pass in the data that will be encoded into the token
        :return: A token
        """
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(days=1)
        to_encode.update({"iat": datetime.now(UTC), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return str(token)

    async def get_email_from_token(self, token: str) -> str:
        """
        The get_email_from_token function takes a token as an argument
        and returns the email address associated with that token.
        The function uses the jwt library to decode the token, which is then used to return the email address.

        :param token: str: Pass in the token that is sent to the user's email address
        :return: The email address of the user who is currently logged in
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return str(email)
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            ) from e

    async def check_date_token(self, token: str) -> bool:
        """
        Validate the expiration date of a given JWT token. If the token is expired, an HTTP 403 error is raised.

        :param token: str: The JWT token to be validated.
        :return: bool: True if the token is valid and not expired.
        :raises HTTPException: If the token is expired (status code: 403) or invalid (status code: 422).
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            expire = payload["exp"]
            expire = datetime.fromtimestamp(expire, tz=UTC)
            if expire < datetime.now(UTC):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token for email verification",
                )
            return True
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            ) from e


security_service = SecurityService()
