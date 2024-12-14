from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.orm import SqlAlchemyBase

if TYPE_CHECKING:
    from src.users.orm import User

class Event(SqlAlchemyBase):
    __tablename__ = "events"

    event_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))
    event_date: Mapped[datetime] = mapped_column()
    location: Mapped[str] = mapped_column(String(255))
    organizer: Mapped[str] = mapped_column(String(100))
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))

    author: Mapped["User"] = relationship(back_populates="created_events")
    registrations: Mapped["EventRegistration"] = relationship(back_populates="event")


class EventRegistration(SqlAlchemyBase):
    __tablename__ = "event_registrations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )
    event_id: Mapped[int] = mapped_column(ForeignKey("events.event_id"))

    user: Mapped["User"] = relationship(back_populates="registrations")
    event: Mapped["Event"] = relationship(back_populates="registrations")
