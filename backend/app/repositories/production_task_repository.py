from sqlalchemy.orm import Session

from app.models.production_task import ProductionTask


class ProductionTaskRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        document_id: int,
        decision_id: int,
        title: str,
        description: str,
        department: str | None = None,
        assigned_person: str | None = None,
        status: str = "pending",
        priority: str = "medium",
    ) -> ProductionTask:
    
        task = ProductionTask(
            document_id=document_id,
            decision_id=decision_id,
            title=title,
            description=description,
            department=department,
            assigned_person=assigned_person,
            status=status,
            priority=priority,
        )
    
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
    
        return task

    def get_by_id(
        self,
        task_id: int,
    ) -> ProductionTask | None:

        return (
            self.db.query(ProductionTask)
            .filter(
                ProductionTask.id == task_id
            )
            .first()
        )

    def get_by_document(
        self,
        document_id: int,
    ) -> list[ProductionTask]:

        return (
            self.db.query(ProductionTask)
            .filter(
                ProductionTask.document_id == document_id
            )
            .order_by(
                ProductionTask.created_at.desc()
            )
            .all()
        )

    def update(
        self,
        task: ProductionTask,
        **values,
    ) -> ProductionTask:

        for field, value in values.items():
            if value is not None:
                setattr(task, field, value)

        self.db.commit()
        self.db.refresh(task)

        return task
