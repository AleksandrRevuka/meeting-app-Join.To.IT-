from src.events.schemas import EventModel, EventRegistrationModel
from src.adapters.repository import AsyncRepository
from src.events.orm import Event, EventRegistration


class EventsRepository(AsyncRepository[Event, EventModel]):
    model = Event
    schema = EventModel

class EventsRegistrationRepository(
    AsyncRepository[EventRegistration, EventRegistrationModel]
):
    model = EventRegistration
    schema = EventRegistrationModel
