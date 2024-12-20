from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI

from src.config.db_config import database_config as db_config
from src.container import Container
from src.events.exceptions.event_exc_handler import event_exception_handler
from src.events.routers import event_routers, event_reg_routers
from src.users.exceptions.auth_exc_handler import auth_exception_handler
from src.users.exceptions.user_exc_handler import user_exception_handler
from src.users.routers.auth_routers import public_router
from src.users.routers.users_routers import user_router

exception_handlers = [
    user_exception_handler,
    auth_exception_handler,
    event_exception_handler,
]

routers = [
    public_router,
    user_router,
    event_routers.public_router,
    event_routers.organizer_router,
    event_reg_routers.user_router,
]

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    The lifespan function is a coroutine that will be called when the application starts up and shut down.
    It's used to create an instance of AsyncIOScheduler, which is then stored in app.state for use by other functions.

    :param app: FastAPI: Pass the fastapi object to the lifespan function
    :return: A context manager, which is used to manage the lifespan of a resource
    """

    container: Container = Container()
    app.container = container
    container.check_dependencies()

    db = container.db_manager()
    await db.connect(echo=db_config.DATABASE_ECHO)
    await db.create_database()
    db.init_session_factory()

    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan)
router = APIRouter()

for handler in exception_handlers:
    handler(app)

for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True)