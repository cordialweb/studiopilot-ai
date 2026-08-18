from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text

from app.models.base import Base
from app.models.mixins import TimestampMixin


class ProducerObservation(Base, TimestampMixin):
    __tablename__ = "producer_observations"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
    )

    type = Column(String(50), nullable=False)

    severity = Column(String(20), nullable=False)

    title = Column(String(255), nullable=False)

    description = Column(Text, nullable=False)

    basis_type = Column(String(20), nullable=False)

    basis = Column(Text, nullable=False, default="")

    scene_number = Column(Integer, nullable=True)

    confidence = Column(Float, nullable=False, default=1.0)

    requires_human_decision = Column(
        Boolean,
        nullable=False,
        default=False,
    )
    
    decision_status = Column(
        String(30),
        nullable=False,
        default="pending",
    )
