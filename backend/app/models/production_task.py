from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.models.base import Base
from app.models.mixins import TimestampMixin


class ProductionTaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProductionTaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ProductionTask(Base, TimestampMixin):

    __tablename__ = "production_tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
    )

    decision_id = Column(
        Integer,
        ForeignKey("producer_decisions.id"),
        nullable=False,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    department = Column(
        String(100),
        nullable=True,
    )

    assigned_person = Column(
        String(255),
        nullable=True,
    )

    status = Column(
        String(30),
        nullable=False,
        default=ProductionTaskStatus.PENDING.value,
    )

    priority = Column(
        String(20),
        nullable=False,
        default=ProductionTaskPriority.MEDIUM.value,
    )