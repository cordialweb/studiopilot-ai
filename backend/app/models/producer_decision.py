from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean

from app.models.base import Base
from app.models.mixins import TimestampMixin


class ProducerDecisionStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    RESOLVED = "resolved"


class ProducerDecisionType:
    APPROVE = "approve"
    REJECT = "reject"
    DEFER = "defer"
    REQUEST_REVIEW = "request_review"


class ProducerDecision(Base, TimestampMixin):
    __tablename__ = "producer_decisions"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Relationships
    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
    )

    observation_id = Column(
        Integer,
        ForeignKey("producer_observations.id"),
        nullable=False,
    )

    # Decision
    decision = Column(
        String(50),
        nullable=True,
    )

    status = Column(
        String(30),
        nullable=False,
        default=ProducerDecisionStatus.PENDING,
    )

    # Producer notes
    notes = Column(
        Text,
        nullable=True,
    )

    # Responsibility
    assigned_department = Column(
        String(100),
        nullable=True,
    )

    assigned_person = Column(
        String(255),
        nullable=True,
    )

