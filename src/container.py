from dependency_injector import containers, providers

from src.events.uow import EventsStorageUnitOfWork
from src.adapters.db.db_manager import AsyncDatabaseSQLAlchemyManager
from src.config.db_config import database_config as db_config
from src.users.uow import UsersStorageUnitOfWork
from src.users.auth_service import AuthUsersService
from src.users.service import UsersService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.users.routers",
        ],
        modules=[
            "src.common.security",
        ],
    )
    db_manager = providers.Singleton(
        AsyncDatabaseSQLAlchemyManager, db_uri=db_config.GET_ASYNC_DB_URL
    )

    users_storege_unit_of_work = providers.Singleton(
        UsersStorageUnitOfWork,
        session_factory=db_manager.provided.session_factory,
    )

    events_storege_unit_of_work = providers.Singleton(
        EventsStorageUnitOfWork,
        session_factory=db_manager.provided.session_factory,
    )

    auth_service = providers.Factory(
        AuthUsersService,
        uow=users_storege_unit_of_work,
    )
    users_service = providers.Factory(
        UsersService,
        uow=users_storege_unit_of_work,
    )