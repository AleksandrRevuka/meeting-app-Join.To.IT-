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
    async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Header for catching special exceptions
        and forming a single response for the user.
        """
        exception_status_map = {
            user_err.UserWithEmailAlreadyExistsError: 409,
            user_err.UserWithPhoneAlreadyExistsError: 409,
            user_err.UserNotFoundError: 404,
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
