from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.common.schemas import ErrorResponse
from src.events.exceptions import event_exceptions as event_err
from src.users.exceptions.auth_exc_handler import exc_name


def event_exception_handler(
    app: FastAPI,
) -> Callable[[Request, Exception], Coroutine[Any, Any, JSONResponse]]:
    @app.exception_handler(event_err.ForbiddenError)
    @app.exception_handler(event_err.EventNotFoundError)
    @app.exception_handler(event_err.RegistrationAlreadyExistsError)
    async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Header for catching special exceptions
        and forming a single response for the user.
        """
        exception_status_map = {
            event_err.EventNotFoundError: 404,
            event_err.ForbiddenError: 403,
            event_err.RegistrationAlreadyExistsError: 400,
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
