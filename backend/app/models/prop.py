from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base
from app.models.mixins import TimestampMixin


class Prop(Base, TimestampMixin):
    __tablename__ = "props"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
    )

    name = Column(String(255), nullable=False)

    category = Column(String(100), nullable=True)

    description = Column(String(1000), nullable=True)

    scenes = Column(
        JSONB,
        nullable=False,
        default=list,
    )

    scene_count = Column(
        Integer,
        default=0,
    )