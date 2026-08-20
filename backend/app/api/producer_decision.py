from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.producer_decision import (
    ProducerDecisionCreate,
    ProducerDecisionListResponse,
    ProducerDecisionResponse,
    ProducerDecisionStatus,
    ProducerDecisionUpdate,
)
from app.services.producer_decision_service import (
    ProducerDecisionService,
)


router = APIRouter(
    tags=["Producer Decisions"],
)


@router.post(
    "/documents/{document_id}/producer-decisions",
    response_model=ProducerDecisionResponse,
)
def create_producer_decision(
    document_id: int,
    data: ProducerDecisionCreate,
    db: Session = Depends(get_db),
):
    service = ProducerDecisionService(db)

    try:
        decision = service.create_decision(
            document_id=document_id,
            observation_id=data.observation_id,
            decision=(
                data.decision.value
                if data.decision
                else None
            ),
            notes=data.notes,
            assigned_department=data.assigned_department,
            assigned_person=data.assigned_person,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return decision

@router.get(
    "/documents/{document_id}/producer-decisions",
    response_model=ProducerDecisionListResponse,
)
def list_producer_decisions(
    document_id: int,
    db: Session = Depends(get_db),
):
    service = ProducerDecisionService(db)

    decisions = service.list_decisions(document_id)

    return {
        "document_id": document_id,
        "count": len(decisions),
        "decisions": decisions,
    }


@router.get(
    "/producer-decisions/{decision_id}",
    response_model=ProducerDecisionResponse,
)
def get_producer_decision(
    decision_id: int,
    db: Session = Depends(get_db),
):
    service = ProducerDecisionService(db)

    decision = service.get_decision(decision_id)

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Producer decision not found",
        )

    return decision


@router.patch(
    "/producer-decisions/{decision_id}",
    response_model=ProducerDecisionResponse,
)
def update_producer_decision(
    decision_id: int,
    data: ProducerDecisionUpdate,
    db: Session = Depends(get_db),
):
    service = ProducerDecisionService(db)

    producer_decision = service.get_decision(decision_id)

    if not producer_decision:
        raise HTTPException(
            status_code=404,
            detail="Producer decision not found",
        )

    if data.status is not None:
        producer_decision.status = data.status.value

    if data.decision is not None:
        producer_decision.decision = data.decision.value

    if data.notes is not None:
        producer_decision.notes = data.notes

    if data.assigned_department is not None:
        producer_decision.assigned_department = (
            data.assigned_department
        )

    if data.assigned_person is not None:
        producer_decision.assigned_person = (
            data.assigned_person
        )

    return service.update_decision(producer_decision)