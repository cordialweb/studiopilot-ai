from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base
from app.models.mixins import TimestampMixin


class Scene(Base, TimestampMixin):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
    )

    scene_number = Column(Integer, nullable=False)

    heading = Column(String(255), nullable=False)

    location = Column(String(255), nullable=False)

    time_of_day = Column(String(50), nullable=True)

    page_start = Column(Integer, nullable=True)

    page_end = Column(Integer, nullable=True)

    summary = Column(String(2000), nullable=True)

    characters = Column(
        JSONB,
        nullable=False,
        default=list,
    )

    props = Column(
        JSONB,
        nullable=False,
        default=list,
    )