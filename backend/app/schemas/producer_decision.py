from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ProducerDecisionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    RESOLVED = "resolved"


class ProducerDecisionType(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    DEFER = "defer"
    REQUEST_REVIEW = "request_review"


class ProducerDecisionCreate(BaseModel):
    observation_id: int
    decision: ProducerDecisionType | None = None
    notes: str | None = None
    assigned_department: str | None = None
    assigned_person: str | None = None


class ProducerDecisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    observation_id: int
    decision: str | None
    status: ProducerDecisionStatus
    notes: str | None
    assigned_department: str | None
    assigned_person: str | None
    created_at: datetime
    updated_at: datetime


class ProducerDecisionListResponse(BaseModel):
    document_id: int
    count: int
    decisions: list[ProducerDecisionResponse]

class ProducerDecisionUpdate(BaseModel):
    status: ProducerDecisionStatus | None = None
    decision: ProducerDecisionType | None = None
    notes: str | None = None
    assigned_department: str | None = None
    assigned_person: str | None = None