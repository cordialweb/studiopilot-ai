from enum import Enum

from pydantic import BaseModel


class ProducerActionCategory(str, Enum):
    HIGH_RISK = "high_risk"
    HUMAN_DECISION = "human_decision"
    PENDING_TASK = "pending_task"
    IN_PROGRESS_TASK = "in_progress_task"


class ProducerActionQueueItem(BaseModel):
    category: ProducerActionCategory
    priority: str

    source_type: str
    source_id: int

    title: str
    description: str

    document_id: int
    scene_number: int | None = None

    assigned_department: str | None = None
    assigned_person: str | None = None


class ProducerActionQueueResponse(BaseModel):
    document_id: int
    count: int
    items: list[ProducerActionQueueItem]
