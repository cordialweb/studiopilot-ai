from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.document import Document
from app.repositories.producer_observation_repository import (
    ProducerObservationRepository,
)
from app.repositories.producer_decision_repository import (
    ProducerDecisionRepository,
)
from app.repositories.production_task_repository import (
    ProductionTaskRepository,
)
from app.schemas.production_overview import ProductionOverviewResponse


router = APIRouter(
    prefix="/documents",
    tags=["Production Overview"],
)


@router.get(
    "/{document_id}/production-overview",
    response_model=ProductionOverviewResponse,
)
def get_production_overview(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    observation_repository = ProducerObservationRepository(db)
    decision_repository = ProducerDecisionRepository(db)
    task_repository = ProductionTaskRepository(db)

    observations = observation_repository.list_by_document(
        document_id
    )

    decisions = decision_repository.list_by_document(
        document_id
    )

    tasks = task_repository.get_by_document(
        document_id
    )

    summary = {
        "observations": len(observations),
        "pending_observations": sum(
            1
            for observation in observations
            if observation.decision_status == "pending"
        ),
        "decided_observations": sum(
            1
            for observation in observations
            if observation.decision_status == "decided"
        ),

        "decisions": len(decisions),
        "pending_decisions": sum(
            1
            for decision in decisions
            if decision.status == "pending"
        ),
        "approved_decisions": sum(
            1
            for decision in decisions
            if decision.status == "approved"
        ),
        "rejected_decisions": sum(
            1
            for decision in decisions
            if decision.status == "rejected"
        ),
        "deferred_decisions": sum(
            1
            for decision in decisions
            if decision.status == "deferred"
        ),
        "resolved_decisions": sum(
            1
            for decision in decisions
            if decision.status == "resolved"
        ),

        "tasks": len(tasks),
        "pending_tasks": sum(
            1
            for task in tasks
            if task.status == "pending"
        ),
        "in_progress_tasks": sum(
            1
            for task in tasks
            if task.status == "in_progress"
        ),
        "completed_tasks": sum(
            1
            for task in tasks
            if task.status == "completed"
        ),
        "cancelled_tasks": sum(
            1
            for task in tasks
            if task.status == "cancelled"
        ),
    }

    return {
        "document_id": document_id,
        "summary": summary,
        "observations": observations,
        "decisions": decisions,
        "tasks": tasks,
    }
