
from datetime import UTC, datetime
import enum

from sqlalchemy import (
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class SqlAlchemyBase(DeclarativeBase):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )


class Role(enum.Enum):
    admin: str = "admin"
    user: str = "user"