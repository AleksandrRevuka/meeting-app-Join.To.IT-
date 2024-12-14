import uuid
from src.events.schemas import CreateEventRegistration, EventCreate, EventModel, EventRegistrationModel, EventUpdate
from src.events.uow import EventsStorageUnitOfWork
from src.events.exceptions import event_exceptions as event_err


class EventsService:
    def __init__(self, uow: EventsStorageUnitOfWork):
        self.uow = uow

    async def get_events(self) -> list[EventModel]:
        async with self.uow:
            events = await self.uow.events.get_all()
        return events
    
    async def get_event_by_id(self, event_id: int) -> EventModel:
        async with self.uow:
            event = await self.uow.events.get_one(event_id=event_id)
            if event is None:
                raise event_err.EventNotFoundError()
            return event
        
    async def create_event(self, body: EventCreate, user_id: uuid.UUID) -> EventModel:
        async with self.uow:
            data = body.model_dump()
            data["author_id"] = user_id

            event = await self.uow.events.add_one(data=data)
            await self.uow.commit()
            return event
            
    async def update_event(self, event_id: int, user_id: uuid.UUID, body: EventUpdate) -> EventModel:
        async with self.uow:
            event = await self.uow.events.get_one(event_id=event_id)
            if event is None:
                raise event_err.EventNotFoundError()
            data = body.model_dump()
            data["author_id"] = user_id
            updated_event = await self.uow.events.update_one(
                data=data, event_id=event_id
            )
            await self.uow.commit()
        return updated_event
    
    async def remove_user(self, event_id: int) -> None:
        async with self.uow:
            event = await self.uow.events.get_one(event_id=event_id)
            if event is None:
                raise event_err.EventNotFoundError()
            
            await self.uow.events.delete_one(event_id=event_id)
            await self.uow.commit()

    async def get_all_registrations(
        self, user_id: uuid.UUID
    ) -> list[EventRegistrationModel]:
        async with self.uow:
            registrations = await self.uow.registrations.get_all(
                user_id=user_id
            )
            return registrations

    async def create_registration(
        self, body: CreateEventRegistration, user_id: uuid.UUID
    ) -> tuple[EventRegistrationModel, EventModel]:
        async with self.uow:
            event = await self.uow.events.get_one(event_id=body.event_id)
            if event is None:
                raise event_err.EventNotFoundError()
            
            existing_registration = await self.uow.registrations.get_one(
                user_id=user_id, event_id=body.event_id
            )
            if existing_registration:
                raise event_err.RegistrationAlreadyExistsError()

            data = body.model_dump()
            data["user_id"] = user_id
            registration = await self.uow.registrations.add_one(data)
            await self.uow.commit()
            event = await self.uow.events.get_one(event_id=registration.event_id)
            if event is None:
                raise event_err.EventNotFoundError()
            return registration, event

    async def delete_registration(
        self, registration_id: int, user_id: uuid.UUID
    ) -> None:
        async with self.uow:
            registration = await self.uow.registrations.get_one(
                id=registration_id, user_id=user_id
            )
            if registration is None:
                raise event_err.ForbiddenError()

            await self.uow.registrations.delete_one(id=registration_id)
            await self.uow.commit()