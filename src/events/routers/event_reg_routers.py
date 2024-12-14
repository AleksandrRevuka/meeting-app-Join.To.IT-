from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from dependency_injector.wiring import Provide, inject
from src.adapters.email import send_event_registration_email
from src.common.security import security_service as auth_service
from src.events.schemas import CreateEventRegistration, EventRegistrationResponse
from src.users.schemas import PrivateUser
from src.container import Container
from src.events.service import EventsService

user_router = APIRouter(prefix="/registrations", tags=["Event Registrations"])


@user_router.get(
    "/",
    response_model=list[EventRegistrationResponse],
    responses={
        status.HTTP_200_OK: {
            "model": list[EventRegistrationResponse],
            "description": "Registration list retrieved successfully.",
        },
    },
)
@inject
async def get_registrations(
    events_service: EventsService = Depends(Provide(Container.events_service)),
    current_user: PrivateUser = Depends(auth_service.get_current_user),
) -> list[EventRegistrationResponse]:
    """
    ## Get all registrations
    """
    registrations = await events_service.get_all_registrations(current_user.user_id)
    return registrations


@user_router.post(
    "/create",
    response_model=EventRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": EventRegistrationResponse,
            "description": "Registration created successfully.",
        },
    },
)
@inject
async def create_registration(
    body: CreateEventRegistration,
    background_tasks: BackgroundTasks,
    request: Request,
    events_service: EventsService = Depends(Provide(Container.events_service)),
    current_user: PrivateUser = Depends(auth_service.get_current_user),
) -> EventRegistrationResponse:
    """
    ## Create a registration
    """
    registration, event = await events_service.create_registration(body, current_user.user_id)
    background_tasks.add_task(
        send_event_registration_email,
        current_user.email,
        event.title,
        event.event_date,
        str(request.base_url),
    )
    return registration


@user_router.delete(
    "/{registration_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Registration deleted successfully.",
        },
    },
)
@inject
async def delete_registration(
    registration_id: int,
    events_service: EventsService = Depends(Provide(Container.events_service)),
    current_user: PrivateUser = Depends(auth_service.get_current_user),
) -> None:
    """
    ## Delete a registration
    """
    await events_service.delete_registration(registration_id, current_user.user_id)
    return None
