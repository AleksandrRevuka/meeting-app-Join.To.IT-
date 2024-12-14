from typing import TYPE_CHECKING
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String

from src.adapters.orm import Role, SqlAlchemyBase

if TYPE_CHECKING:
    from src.events.orm import Event, EventRegistration


class User(SqlAlchemyBase):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    username: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str | None] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    role: Mapped[Role] = mapped_column(default=Role.user)

    created_events: Mapped[list["Event"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    registrations: Mapped[list["EventRegistration"]] = relationship(back_populates="user")