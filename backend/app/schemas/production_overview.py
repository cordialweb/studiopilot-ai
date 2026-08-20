from pydantic import BaseModel

from app.schemas.producer_observation import ProducerObservationResponse
from app.schemas.producer_decision import ProducerDecisionResponse
from app.schemas.production_task import ProductionTaskResponse


class ProductionOverviewSummary(BaseModel):
    observations: int
    pending_observations: int
    decided_observations: int

    decisions: int
    pending_decisions: int
    approved_decisions: int
    rejected_decisions: int
    deferred_decisions: int
    resolved_decisions: int

    tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completed_tasks: int
    cancelled_tasks: int


class ProductionOverviewResponse(BaseModel):
    document_id: int
    summary: ProductionOverviewSummary

    observations: list[ProducerObservationResponse]
    decisions: list[ProducerDecisionResponse]
    tasks: list[ProductionTaskResponse]
