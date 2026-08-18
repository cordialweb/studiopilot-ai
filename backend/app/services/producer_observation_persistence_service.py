from sqlalchemy.orm import Session

from app.models.producer_observation import ProducerObservation
from app.schemas.producer_observation import ProducerObservationResultV1


class ProducerObservationPersistenceService:

    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        document_id: int,
        result: ProducerObservationResultV1,
    ):
        for observation in result.observations:
            db_observation = ProducerObservation(
                document_id=document_id,
                type=observation.type,
                severity=observation.severity,
                title=observation.title,
                description=observation.description,
                basis_type=observation.basis_type,
                basis=observation.basis,
                scene_number=observation.scene_number,
                confidence=observation.confidence,
                requires_human_decision=observation.requires_human_decision,
            )

            self.db.add(db_observation)

        self.db.commit()

        return result
