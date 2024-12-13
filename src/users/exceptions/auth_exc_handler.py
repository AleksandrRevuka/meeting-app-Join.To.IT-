from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.common.schemas import ErrorResponse

from src.users.exceptions import auth_exceptions as auth_err


def exc_name(ex: Exception) -> str:
    return f"{ex.__class__.__name__}: {ex}"


def auth_exception_handler(
    app: FastAPI,
) -> Callable[[Request, Exception], Coroutine[Any, Any, JSONResponse]]:
    @app.exception_handler(auth_err.InvalidPasswordError)
    @app.exception_handler(auth_err.EmailNotConfirmedError)
    @app.exception_handler(auth_err.UserNotFoundUnAuthorizedError)
    @app.exception_handler(auth_err.InvalidRefreshTokenError)
    @app.exception_handler(auth_err.InvalidTokenError)
    @app.exception_handler(auth_err.PasswordsNotMatchingError)
    @app.exception_handler(auth_err.EmailAlreadyConfirmedError)
    @app.exception_handler(auth_err.InvalidResetPasswordTokenError)
    @app.exception_handler(auth_err.ForbiddenError)
    async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Header for catching special exceptions
        and forming a single response for the user.
        """
        exception_status_map = {
            auth_err.InvalidPasswordError: 401,
            auth_err.EmailNotConfirmedError: 401,
            auth_err.UserNotFoundUnAuthorizedError: 401,
            auth_err.InvalidRefreshTokenError: 401,
            auth_err.InvalidTokenError: 403,
            auth_err.PasswordsNotMatchingError: 400,
            auth_err.EmailAlreadyConfirmedError: 400,
            auth_err.InvalidResetPasswordTokenError: 403,
            auth_err.ForbiddenError: 403,
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
