from enum import Enum
from typing import Literal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ObservationType(str, Enum):
    REQUIREMENT = "REQUIREMENT"
    RISK = "RISK"
    DEPENDENCY = "DEPENDENCY"
    OVERLOOKED_ITEM = "OVERLOOKED_ITEM"
    DECISION = "DECISION"


class ObservationSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    
class ProducerObservationDecisionStatus(str, Enum):
    PENDING = "pending"
    DECIDED = "decided"
    NOT_REQUIRED = "not_required"


class ProducerObservationV1(BaseModel):
    type: ObservationType

    severity: ObservationSeverity = ObservationSeverity.MEDIUM

    title: str = Field(
        ...,
        description="Short producer-facing observation title",
    )

    description: str = Field(
        ...,
        description="Evidence-based explanation of the observation",
    )

    basis_type: Literal["EXPLICIT", "INFERRED"] = "EXPLICIT"

    basis: str = Field(
        default="",
        description="Screenplay evidence supporting the observation",
    )

    scene_number: int | None = Field(
        default=None,
        description="Related scene number when applicable",
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence that the observation is supported by the screenplay",
    )

    requires_human_decision: bool = False


class ProducerObservationResultV1(BaseModel):
    observations: list[ProducerObservationV1] = Field(
        default_factory=list
    )


class ProducerObservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    type: str
    severity: str
    title: str
    description: str
    basis_type: str
    basis: str
    scene_number: int | None
    confidence: float
    requires_human_decision: bool
    decision_status: ProducerObservationDecisionStatus
    created_at: datetime
    updated_at: datetime


class ProducerObservationListResponse(BaseModel):
    document_id: int
    count: int
    observations: list[ProducerObservationResponse]