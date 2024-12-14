from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from src.events.schemas import EventCreate, EventResponse, EventUpdate
from src.adapters.orm import Role
from src.events.service import EventsService
from src.common.security import security_service as auth_service
from src.container import Container
from src.users.schemas import PrivateUser
from src.events.exceptions import event_exceptions as event_exc

organizer_router = APIRouter(prefix="/events", tags=["Events: <CRUD>"])
public_router = APIRouter(prefix="/events", tags=["Events: <CRUD>"])


@public_router.get(
    "/",
    response_model=list[EventResponse],
    responses={
        status.HTTP_200_OK: {
            "model": list[EventResponse],
            "description": "Event list received successfully.",
        },
    },
)
@inject
async def read_events(
    events_service: EventsService = Depends(Provide(Container.events_service)),
) -> list[EventResponse]:
    """
    ## Get events
    """
    
    events: list[EventResponse] = await events_service.get_events()
    
    return events


@public_router.get(
    "/{event_id}",
    response_model=EventResponse,
    responses={
        status.HTTP_200_OK: {
            "model": EventResponse,
            "description": "Event received successfully.",
        },
    },
)
@inject
async def read_event(
    event_id: int,
    events_service: EventsService = Depends(Provide(Container.events_service)),
) -> EventResponse:
    """
    ## Get event
    """
    event: EventResponse = await events_service.get_event_by_id(event_id=event_id)

    return event


@organizer_router.post(
    "/create",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": EventResponse,
            "description": "Creates something from user request.",
        },
    },
)
@inject
async def create_event(
    body: EventCreate,
    events_service: EventsService = Depends(Provide(Container.events_service)),
    current_user: PrivateUser = Depends(auth_service.get_current_user),
) -> EventResponse:
    """
    ## Sign up a new user.
    """
    if current_user.role == Role.organizer:
        new_event: PrivateUser = await events_service.create_event(body, current_user.user_id)
    else:
        raise event_exc.ForbiddenError()
    return new_event


@organizer_router.put(
    "/{event_id}",
    response_model=EventResponse,
)
@inject
async def update_event(
    event_id: int,
    body: EventUpdate,
    events_service: EventsService = Depends(Provide(Container.events_service)),
    current_user: PrivateUser = Depends(auth_service.get_current_user),
) -> EventResponse:
    if current_user.role == Role.organizer:
        updated_event: EventResponse = await events_service.update_event(event_id, current_user.user_id, body)
    else:
        raise event_exc.ForbiddenError()
    return updated_event


@organizer_router.delete(
    "/{event_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def remove_event(
    event_id: int,
    events_service: EventsService = Depends(Provide(Container.events_service)),
    current_user: PrivateUser = Depends(auth_service.get_current_user),
) -> None:
    """
    ## Delete event
    """
    if current_user.role == Role.organizer:
        await events_service.remove_user(event_id)
    else:
        raise event_exc.ForbiddenError()
    return None
