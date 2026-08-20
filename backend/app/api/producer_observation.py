from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.producer_observation import (
    ProducerObservationListResponse,
    ProducerObservationResponse,
)
from app.services.producer_observation_read_service import (
    ProducerObservationReadService,
)


router = APIRouter(
    prefix="/documents",
    tags=["Producer Observations"],
)


@router.get(
    "/{document_id}/producer-observations",
    response_model=ProducerObservationListResponse,
)
def list_producer_observations(
    document_id: int,
    db: Session = Depends(get_db),
):
    service = ProducerObservationReadService(db)

    observations = service.list_by_document(document_id)

    return {
        "document_id": document_id,
        "count": len(observations),
        "observations": observations,
    }


@router.get(
    "/{document_id}/producer-observations/{observation_id}",
    response_model=ProducerObservationResponse,
)
def get_producer_observation(
    document_id: int,
    observation_id: int,
    db: Session = Depends(get_db),
):
    service = ProducerObservationReadService(db)

    observation = service.get_for_document(
        observation_id=observation_id,
        document_id=document_id,
    )

    if not observation:
        raise HTTPException(
            status_code=404,
            detail="Producer observation not found",
        )

    return observation