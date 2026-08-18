from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.mixins import TimestampMixin


class Character(Base, TimestampMixin):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    aliases: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    age: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    occupation: Mapped[str] = mapped_column(
        String(255),
        default="",
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        default="",
    )

    scenes: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    first_scene: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    last_scene: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )