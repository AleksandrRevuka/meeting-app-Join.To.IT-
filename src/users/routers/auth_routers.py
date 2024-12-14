from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from starlette.responses import HTMLResponse, RedirectResponse

from src.adapters.orm import Role
from src.container import Container

from src.users.auth_service import AuthUsersService
from src.users.schemas import PrivateUser, TokenModel, UserCreate, UserResponse
from src.users.utils import get_password_hash

public_router = APIRouter(prefix="/auth", tags=["Users: Authentication"])

security = HTTPBearer()


@public_router.post(
    "/signup_user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": UserResponse,
            "description": "Creates something from user request.",
        },
    },
)
@inject
async def signup_user(
    body: UserCreate,
    auth_user_service: AuthUsersService = Depends(Provide(Container.auth_service)),
) -> UserResponse:
    """
    ## Sign up a new user.
    """
    body.password = get_password_hash(body.password)
    new_user: PrivateUser = await auth_user_service.create_user(body)

    return new_user


@public_router.post(
    "/login",
    response_model=TokenModel,
    responses={
        status.HTTP_200_OK: {
            "model": TokenModel,
            "description": "Successful login, returns access and refresh tokens.",
        },
    },
)
@inject
async def login(
    auth_user_service: AuthUsersService = Depends(Provide(Container.auth_service)),
    body: OAuth2PasswordRequestForm = Depends(),
) -> TokenModel:
    """
    ## User login.
    """
    token_result: TokenModel = await auth_user_service.user_login(
        body.username, body.password
    )

    return token_result


@public_router.get(
    "/logout",
    response_class=HTMLResponse,
    responses={
        status.HTTP_302_FOUND: {
            "description": "Redirects to login page and deletes access token cookie."
        }
    },
)
async def logout() -> RedirectResponse:
    """
    ## User logout.
    """
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")

    return response

