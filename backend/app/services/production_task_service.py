from sqlalchemy.orm import Session

from app.models.producer_decision import ProducerDecision
from app.models.production_task import ProductionTask
from app.repositories.production_task_repository import (
    ProductionTaskRepository,
)


class ProductionTaskService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = ProductionTaskRepository(db)

    def create_task(
        self,
        *,
        document_id: int,
        decision_id: int,
        title: str,
        description: str,
        department: str | None = None,
        assigned_person: str | None = None,
        priority: str = "medium",
    ) -> ProductionTask:

        decision = (
            self.db.query(ProducerDecision)
            .filter(
                ProducerDecision.id == decision_id,
                ProducerDecision.document_id == document_id,
            )
            .first()
        )

        if not decision:
            raise ValueError(
                "Producer decision not found for this document."
            )

        return self.repository.create(
            document_id=document_id,
            decision_id=decision_id,
            title=title,
            description=description,
            department=department,
            assigned_person=assigned_person,
            priority=priority,
        )

    def get_task(
        self,
        task_id: int,
    ) -> ProductionTask | None:

        return self.repository.get_by_id(task_id)

    def get_document_tasks(
        self,
        document_id: int,
    ) -> list[ProductionTask]:

        return self.repository.get_by_document(document_id)

    def _build_task_from_decision(
        self,
        decision: ProducerDecision,
    ) -> tuple[str, str]:

        notes = (decision.notes or "").strip()
        decision_type = (decision.decision or "").strip()

        # -----------------------------------------
        # REQUEST REVIEW
        # -----------------------------------------

        if decision_type == "request_review":

            if notes:
                title = self._make_review_title(notes)

                description = (
                    f"Review the following production decision: "
                    f"{notes} "
                    f"Evaluate the available production approaches "
                    f"and provide a recommendation before the decision "
                    f"is finalized."
                )

                return title, description

            return (
                "Review producer decision",
                "Review the producer decision and provide a "
                "production recommendation before final approval."
            )

        # -----------------------------------------
        # APPROVE
        # -----------------------------------------

        if decision_type == "approve":

            if notes:
                return (
                    f"Execute approved decision: {notes}",
                    f"Proceed with the approved production decision: "
                    f"{notes}"
                )

            return (
                "Execute approved production decision",
                "Proceed with the approved production decision."
            )

        # -----------------------------------------
        # REJECT
        # -----------------------------------------

        if decision_type == "reject":

            if notes:
                return (
                    f"Resolve rejected decision: {notes}",
                    f"Review the rejected decision and determine "
                    f"the required alternative production approach: "
                    f"{notes}"
                )

            return (
                "Resolve rejected production decision",
                "Determine the required alternative approach "
                "for the rejected production decision."
            )

        # -----------------------------------------
        # DEFER
        # -----------------------------------------

        if decision_type == "defer":

            if notes:
                return (
                    f"Revisit deferred decision: {notes}",
                    f"Revisit the deferred production decision: "
                    f"{notes}"
                )

            return (
                "Revisit deferred production decision",
                "Revisit the deferred production decision "
                "when the required information is available."
            )

        # -----------------------------------------
        # FALLBACK
        # -----------------------------------------

        if notes:
            return (
                notes,
                f"Review and determine the required production "
                f"action for: {notes}"
            )

        return (
            "Review producer decision",
            "Review the producer decision and determine "
            "the required production action."
        )

    def _make_review_title(
        self,
        notes: str,
    ) -> str:

        text = notes.strip()

        # Remove trailing punctuation
        text = text.rstrip(".!?")

        # Keep title reasonably short
        if len(text) > 100:
            text = text[:97].rstrip() + "..."

        return f"Evaluate: {text}"        
        
    def generate_from_decision(
        self,
        decision: ProducerDecision,
    ) -> ProductionTask:

        # -----------------------------------------
        # Prevent duplicate task generation
        # -----------------------------------------

        existing_tasks = self.repository.get_by_document(
            decision.document_id
        )

        for task in existing_tasks:
            if task.decision_id == decision.id:
                return task

        # -----------------------------------------
        # Generate intelligent task information
        # -----------------------------------------

        title, description = self._build_task_from_decision(
            decision
        )

        # -----------------------------------------
        # Determine department
        # -----------------------------------------

        department = decision.assigned_department

        if not department:
            department = "Production"

        # -----------------------------------------
        # Determine priority
        # -----------------------------------------

        priority = "medium"

        if decision.decision == "request_review":
            priority = "high"

        elif decision.decision == "approve":
            priority = "medium"

        elif decision.decision == "reject":
            priority = "high"

        elif decision.decision == "defer":
            priority = "medium"

        # -----------------------------------------
        # Create production task
        # -----------------------------------------

        task = self.repository.create(
            document_id=decision.document_id,
            decision_id=decision.id,
            title=title,
            description=description,
            department=department,
            assigned_person=decision.assigned_person,
            priority=priority,
        )

        return task
        
    def update_task(
        self,
        task_id: int,
        **values,
    ) -> ProductionTask:
    
        task = self.repository.get_by_id(task_id)
    
        if not task:
            raise ValueError(
                "Production task not found."
            )
    
        # -----------------------------------------
        # Validate status transitions
        # -----------------------------------------
    
        new_status = values.get("status")
    
        if new_status is not None:
    
            current_status = task.status
    
            allowed_transitions = {
                "pending": {
                    "pending",
                    "in_progress",
                    "cancelled",
                },
                "in_progress": {
                    "in_progress",
                    "completed",
                    "cancelled",
                },
                "completed": {
                    "completed",
                },
                "cancelled": {
                    "cancelled",
                },
            }
    
            allowed = allowed_transitions.get(
                current_status,
                set(),
            )
    
            if new_status not in allowed:
                raise ValueError(
                    f"Invalid task status transition: "
                    f"{current_status} -> {new_status}"
                )
    
        # -----------------------------------------
        # Update task
        # -----------------------------------------
    
        task = self.repository.update(
            task,
            **values,
        )
    
        # -----------------------------------------
        # Resolve producer decision
        # when task is completed
        # -----------------------------------------
    
        if (
            new_status == "completed"
            and task.decision_id
        ):
    
            decision = (
                self.db.query(ProducerDecision)
                .filter(
                    ProducerDecision.id == task.decision_id
                )
                .first()
            )
    
            if decision:
                decision.status = "resolved"
                self.db.commit()
                self.db.refresh(decision)
    
        return task
        
    def get_task_decision(
        self,
        task_id: int,
    ) -> ProducerDecision | None:
    
        task = self.repository.get_by_id(task_id)
    
        if not task:
            return None
    
        return (
            self.db.query(ProducerDecision)
            .filter(
                ProducerDecision.id == task.decision_id
            )
            .first()
        )