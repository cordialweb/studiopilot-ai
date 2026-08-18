from sqlalchemy.orm import Session

from app.models.producer_observation import ProducerObservation


class ProducerObservationRepository:

    def __init__(self, db: Session):
        self.db = db

    def list_by_document(
        self,
        document_id: int,
    ) -> list[ProducerObservation]:
        return (
            self.db.query(ProducerObservation)
            .filter(
                ProducerObservation.document_id == document_id
            )
            .order_by(
                ProducerObservation.severity.desc(),
                ProducerObservation.id.asc(),
            )
            .all()
        )
    
    def get_for_document(
        self,
        observation_id: int,
        document_id: int,
    ):
        return (
            self.db.query(ProducerObservation)
            .filter(
                ProducerObservation.id == observation_id,
                ProducerObservation.document_id == document_id,
            )
            .first()
        )
