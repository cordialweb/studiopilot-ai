from sqlalchemy.orm import Session

from app.models.producer_decision import ProducerDecision
from app.repositories.producer_decision_repository import (
    ProducerDecisionRepository,
)
from app.repositories.producer_observation_repository import (
    ProducerObservationRepository,
)
from app.services.production_task_service import ProductionTaskService

class ProducerDecisionService:

    def __init__(self, db: Session):
        self.repository = ProducerDecisionRepository(db)
        self.observation_repository = ProducerObservationRepository(db)

    def _get_observation(
        self,
        document_id: int,
        observation_id: int,
    ):
        observation = self.observation_repository.get_for_document(
            observation_id=observation_id,
            document_id=document_id,
        )

        if not observation:
            raise ValueError(
                "Producer observation not found for this document."
            )

        return observation

    def _sync_status(
        self,
        observation,
        producer_decision,
    ):
        """
        Synchronize ProducerDecision status and
        ProducerObservation decision status.
        """
    
        decision = producer_decision.decision
    
        if decision == "approve":
            producer_decision.status = "approved"
            observation.decision_status = "decided"
    
        elif decision == "reject":
            producer_decision.status = "rejected"
            observation.decision_status = "decided"
    
        elif decision == "defer":
            producer_decision.status = "deferred"
            observation.decision_status = "pending"
    
        elif decision == "request_review":
            producer_decision.status = "pending"
            observation.decision_status = "pending"
    
        else:
            producer_decision.status = "pending"
            observation.decision_status = "pending"

    def create_decision(
        self,
        document_id: int,
        observation_id: int,
        decision: str | None = None,
        notes: str | None = None,
        assigned_department: str | None = None,
        assigned_person: str | None = None,
    ) -> ProducerDecision:
    
        observation = self._get_observation(
            document_id=document_id,
            observation_id=observation_id,
        )
    
        producer_decision = ProducerDecision(
            document_id=document_id,
            observation_id=observation_id,
            decision=decision,
            notes=notes,
            assigned_department=assigned_department,
            assigned_person=assigned_person,
        )
    
        self._sync_status(
            observation,
            producer_decision,
        )
    
        # First save decision so it receives an ID
        producer_decision = self.repository.create(
            producer_decision
        )
    
        # Then generate task using the persisted decision
        if producer_decision.decision == "approve":
            ProductionTaskService(
                self.repository.db
            ).generate_from_decision(
                producer_decision
            )
    
        return producer_decision

    def get_decision(
        self,
        decision_id: int,
    ) -> ProducerDecision | None:

        return self.repository.get(decision_id)

    def list_decisions(
        self,
        document_id: int,
    ) -> list[ProducerDecision]:

        return self.repository.list_by_document(document_id)

    def update_decision(
        self,
        decision: ProducerDecision,
    ) -> ProducerDecision:

        observation = self._get_observation(
            document_id=decision.document_id,
            observation_id=decision.observation_id,
        )

        self._sync_status(
            observation,
            decision,
        )

        return self.repository.update(decision)