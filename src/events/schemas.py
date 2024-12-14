import uuid
from pydantic import BaseModel, Field, PositiveInt, FutureDate

class EventCreate(BaseModel):
    title: str = Field(
        examples=["Tech Conference 2024"],
        min_length=2,
        max_length=255,
        description="The title of the event.",
    )
    description: str | None = Field(
        examples=["An annual conference for tech enthusiasts."],
        default=None,
        min_length=2,
        max_length=255,
        description="A brief description of the event. Optional field.",
    )
    event_date: FutureDate = Field(
        examples=["2024-05-15"],
        description="The date when the event is scheduled to take place.",
    )
    location: str = Field(
        examples=["Kyiv Expo Plaza"],
        min_length=2,
        max_length=255,
        description="The location where the event will be held.",
    )
    organizer: str = Field(
        examples=["Tech Innovators Inc."],
        min_length=2,
        max_length=100,
        description="The name of the individual or organization organizing the event.",
    )


class EventResponse(EventCreate):
    event_id: PositiveInt = Field(
        examples=[1],
        description="Unique identifier for the event.",
    )


class EventUpdate(EventCreate): ...


class EventModel(EventResponse): ...


class CreateEventRegistration(BaseModel):
    event_id: PositiveInt = Field(
        examples=[1],
        description="The unique identifier of the event the user registered for.",
    )


class EventRegistrationResponse(CreateEventRegistration):
    id: PositiveInt = Field(
        examples=[101],
        description="Unique identifier for the event registration.",
    )
    user_id: uuid.UUID = Field(
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="The unique identifier of the user who registered for the event.",
    )



class EventRegistrationModel(EventRegistrationResponse): ...
