from sqlalchemy.orm import Session

from app.repositories.producer_observation_repository import (
    ProducerObservationRepository,
)


class ProducerObservationReadService:

    def __init__(self, db: Session):
        self.repository = ProducerObservationRepository(db)

    def list_by_document(
        self,
        document_id: int,
    ):
        return self.repository.list_by_document(
            document_id
        )

    def get_for_document(
        self,
        observation_id: int,
        document_id: int,
    ):
        return self.repository.get_for_document(
            observation_id=observation_id,
            document_id=document_id,
        )