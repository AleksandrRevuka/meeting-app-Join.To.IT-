import uuid
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from src.common.security import security_service as auth_service
from src.container import Container
from src.users.schemas import PrivateUser, UserResponse
from src.users.service import UsersService

user_router = APIRouter(prefix="/users", tags=["Users: Profile"])


@user_router.get(
    "/me",
    responses={
        status.HTTP_200_OK: {
            "model": UserResponse,
            "description": "Successfully retrieved the user's profile.",
        },
    },
)
@inject
async def read_me(
    users_service: UsersService = Depends(Provide(Container.users_service)),
    current_user: PrivateUser = Depends(auth_service.get_current_user),
) -> UserResponse:
    """
    ## Get Current User Profile
    """
    user: UserResponse = await users_service.get_user_by_id(
            user_id=current_user.user_id
        )
    return user


@user_router.delete(
    "/{user_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_user(
    user_id: uuid.UUID,
    users_service: UsersService = Depends(Provide(Container.users_service)),
) -> None:
    """
    ## Delete User Account
    """
    await users_service.delete_user(user_id)

    return None
