from src.events.schemas import EventsModel, EventsRepositoryModel
from src.adapters.repository import AsyncRepository
from src.events.orm import Event, EventRegistration


class EventsRepository(AsyncRepository[Event, EventsModel]):
    model = Event
    schema = EventsModel

class EventsRegistrationRepository(
    AsyncRepository[EventRegistration, EventsRepositoryModel]
):
    model = EventRegistration
    schema = EventsRepositoryModel
