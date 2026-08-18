from sqlalchemy.orm import Session

from app.models.producer_decision import ProducerDecision


class ProducerDecisionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        decision: ProducerDecision,
    ) -> ProducerDecision:

        self.db.add(decision)
        self.db.commit()
        self.db.refresh(decision)

        return decision

    def get(
        self,
        decision_id: int,
    ) -> ProducerDecision | None:

        return (
            self.db.query(ProducerDecision)
            .filter(
                ProducerDecision.id == decision_id
            )
            .first()
        )

    def list_by_document(
        self,
        document_id: int,
    ) -> list[ProducerDecision]:

        return (
            self.db.query(ProducerDecision)
            .filter(
                ProducerDecision.document_id == document_id
            )
            .order_by(
                ProducerDecision.created_at.desc()
            )
            .all()
        )

    def update(
        self,
        decision: ProducerDecision,
    ) -> ProducerDecision:

        self.db.commit()
        self.db.refresh(decision)

        return decision
