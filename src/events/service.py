from src.events.uow import EventsStorageUnitOfWork


class EventsService:
    def __init__(self, uow: EventsStorageUnitOfWork):
        self.uow = uow