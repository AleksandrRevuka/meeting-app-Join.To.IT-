from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.common.schemas import ErrorResponse
from src.users.exceptions import user_exceptions as user_err
from src.users.exceptions.auth_exc_handler import exc_name


def user_exception_handler(
    app: FastAPI,
) -> Callable[[Request, Exception], Coroutine[Any, Any, JSONResponse]]:
    @app.exception_handler(user_err.UserWithEmailAlreadyExistsError)
    @app.exception_handler(user_err.UserWithPhoneAlreadyExistsError)
    @app.exception_handler(user_err.UserNotFoundError)
    @app.exception_handler(user_err.CannotBanYourselfError)
    @app.exception_handler(user_err.UserAlreadyBannedError)
    @app.exception_handler(user_err.UserNotBannedError)
    @app.exception_handler(user_err.UserBannedError)
    @app.exception_handler(user_err.NewRoleNotSpecifiedError)
    @app.exception_handler(user_err.ForbiddenRoleChangeError)
    @app.exception_handler(user_err.PermissionDeniedError)
    @app.exception_handler(user_err.InvalidFileTypeError)
    @app.exception_handler(user_err.FileTooLargeError)
    @app.exception_handler(user_err.CloudinaryUploadFailedError)
    @app.exception_handler(user_err.CloudinaryFailedUploadAvatarError)
    @app.exception_handler(user_err.OldPasswordNotCorrectError)
    @app.exception_handler(user_err.NewPasswordNotMatchError)
    async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Header for catching special exceptions
        and forming a single response for the user.
        """
        exception_status_map = {
            user_err.UserWithEmailAlreadyExistsError: 409,
            user_err.UserWithPhoneAlreadyExistsError: 409,
            user_err.UserNotFoundError: 404,
            user_err.CannotBanYourselfError: 400,
            user_err.UserAlreadyBannedError: 400,
            user_err.UserNotBannedError: 400,
            user_err.UserBannedError: 403,
            user_err.NewRoleNotSpecifiedError: 403,
            user_err.ForbiddenRoleChangeError: 403,
            user_err.PermissionDeniedError: 403,
            user_err.InvalidFileTypeError: 400,
            user_err.FileTooLargeError: 400,
            user_err.CloudinaryUploadFailedError: 400,
            user_err.OldPasswordNotCorrectError: 400,
            user_err.NewPasswordNotMatchError: 400,
            user_err.CloudinaryFailedUploadAvatarError: 500,
        }

        status_code = exception_status_map.get(type(exc), 500)

        return JSONResponse(
            status_code=status_code,
            content=ErrorResponse.respond(
                message=str(exc),
                exception=exc_name(exc),
            ),
        )

    return custom_exception_handler
