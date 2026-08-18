from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ProductionTaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProductionTaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ProductionTaskCreate(BaseModel):
    decision_id: int = Field(
        ...,
        description="Producer decision that created this production task",
    )

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Short production task title",
    )

    description: str = Field(
        ...,
        min_length=1,
        description="Description of the production task",
    )

    department: str | None = Field(
        default=None,
        max_length=100,
        description="Production department responsible for the task",
    )

    assigned_person: str | None = Field(
        default=None,
        max_length=255,
        description="Person assigned to the task",
    )

    priority: ProductionTaskPriority = Field(
        default=ProductionTaskPriority.MEDIUM,
        description="Task priority",
    )


class ProductionTaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        min_length=1,
    )

    department: str | None = Field(
        default=None,
        max_length=100,
    )

    assigned_person: str | None = Field(
        default=None,
        max_length=255,
    )

    status: ProductionTaskStatus | None = None

    priority: ProductionTaskPriority | None = None


class ProductionTaskResponse(BaseModel):
    id: int
    document_id: int
    decision_id: int

    title: str
    description: str

    department: str | None
    assigned_person: str | None

    status: ProductionTaskStatus
    priority: ProductionTaskPriority

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class ProductionTaskListResponse(BaseModel):
    document_id: int
    count: int
    tasks: list[ProductionTaskResponse] = Field(
        default_factory=list
    )
