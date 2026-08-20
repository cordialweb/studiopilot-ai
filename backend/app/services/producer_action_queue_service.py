from app.repositories.producer_observation_repository import (
    ProducerObservationRepository,
)
from app.repositories.producer_decision_repository import (
    ProducerDecisionRepository,
)
from app.repositories.production_task_repository import (
    ProductionTaskRepository,
)
from app.schemas.producer_action_queue import (
    ProducerActionCategory,
    ProducerActionQueueItem,
)


class ProducerActionQueueService:

    def __init__(self, db):
        self.observation_repository = (
            ProducerObservationRepository(db)
        )

        self.decision_repository = (
            ProducerDecisionRepository(db)
        )

        self.task_repository = (
            ProductionTaskRepository(db)
        )

    def get_queue(
        self,
        document_id: int,
    ) -> list[ProducerActionQueueItem]:

        observations = (
            self.observation_repository.list_by_document(
                document_id
            )
        )

        decisions = (
            self.decision_repository.list_by_document(
                document_id
            )
        )

        tasks = (
            self.task_repository.get_by_document(
                document_id
            )
        )

        items: list[ProducerActionQueueItem] = []

        # -----------------------------------------
        # High-risk observations
        # -----------------------------------------

        for observation in observations:

            if (
                observation.severity == "HIGH"
                and observation.decision_status == "pending"
            ):
                items.append(
                    ProducerActionQueueItem(
                        category=ProducerActionCategory.HIGH_RISK,
                        priority="high",
                        source_type="observation",
                        source_id=observation.id,
                        title=observation.title,
                        description=observation.description,
                        document_id=observation.document_id,
                        scene_number=observation.scene_number,
                    )
                )

        # -----------------------------------------
        # Human decisions
        # -----------------------------------------

        for observation in observations:

            if (
                observation.requires_human_decision
                and observation.decision_status == "pending"
            ):
                items.append(
                    ProducerActionQueueItem(
                        category=ProducerActionCategory.HUMAN_DECISION,
                        priority=observation.severity.lower(),
                        source_type="observation",
                        source_id=observation.id,
                        title=observation.title,
                        description=observation.description,
                        document_id=observation.document_id,
                        scene_number=observation.scene_number,
                    )
                )

        # -----------------------------------------
        # Pending production tasks
        # -----------------------------------------

        for task in tasks:

            if task.status == "pending":

                items.append(
                    ProducerActionQueueItem(
                        category=ProducerActionCategory.PENDING_TASK,
                        priority=task.priority,
                        source_type="production_task",
                        source_id=task.id,
                        title=task.title,
                        description=task.description,
                        document_id=task.document_id,
                        assigned_department=task.department,
                        assigned_person=task.assigned_person,
                    )
                )

        # -----------------------------------------
        # In-progress production tasks
        # -----------------------------------------

        for task in tasks:

            if task.status == "in_progress":

                items.append(
                    ProducerActionQueueItem(
                        category=ProducerActionCategory.IN_PROGRESS_TASK,
                        priority=task.priority,
                        source_type="production_task",
                        source_id=task.id,
                        title=task.title,
                        description=task.description,
                        document_id=task.document_id,
                        assigned_department=task.department,
                        assigned_person=task.assigned_person,
                    )
                )

        # -----------------------------------------
        # Category priority
        # -----------------------------------------

        category_order = {
            ProducerActionCategory.HIGH_RISK: 1,
            ProducerActionCategory.HUMAN_DECISION: 2,
            ProducerActionCategory.PENDING_TASK: 3,
            ProducerActionCategory.IN_PROGRESS_TASK: 4,
        }

        items.sort(
            key=lambda item: (
                category_order[item.category],
                item.source_id,
            )
        )

        return items
