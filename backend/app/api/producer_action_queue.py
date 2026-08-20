from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.producer_action_queue import (
    ProducerActionQueueResponse,
)
from app.services.producer_action_queue_service import (
    ProducerActionQueueService,
)


router = APIRouter(
    prefix="/documents",
    tags=["Producer Action Queue"],
)


@router.get(
    "/{document_id}/action-queue",
    response_model=ProducerActionQueueResponse,
)
def get_producer_action_queue(
    document_id: int,
    db: Session = Depends(get_db),
):
    service = ProducerActionQueueService(db)

    items = service.get_queue(document_id)

    return {
        "document_id": document_id,
        "count": len(items),
        "items": items,
    }
