from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.production_task import (
    ProductionTaskCreate,
    ProductionTaskUpdate,
    ProductionTaskResponse,
    ProductionTaskListResponse,
)
from app.models.producer_decision import ProducerDecision
from app.services.producer_decision_service import ProducerDecisionService
from app.services.production_task_service import ProductionTaskService

router = APIRouter(
    tags=["Production Tasks"],
)


@router.post(
    "/producer-decisions/{decision_id}/generate-task",
    response_model=ProductionTaskResponse,
)
def generate_task_from_decision(
    decision_id: int,
    db: Session = Depends(get_db),
):
    decision_service = ProducerDecisionService(db)

    decision = decision_service.get_decision(decision_id)

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Producer decision not found.",
        )

    task_service = ProductionTaskService(db)

    return task_service.generate_from_decision(decision)

@router.post(
    "/documents/{document_id}/production-tasks",
    response_model=ProductionTaskResponse,
)
def create_production_task(
    document_id: int,
    data: ProductionTaskCreate,
    db: Session = Depends(get_db),
):
    service = ProductionTaskService(db)

    try:
        task = service.create_task(
            document_id=document_id,
            decision_id=data.decision_id,
            title=data.title,
            description=data.description,
            department=data.department,
            assigned_person=data.assigned_person,
            priority=data.priority.value,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    return task


@router.get(
    "/documents/{document_id}/production-tasks",
    response_model=ProductionTaskListResponse,
)
def get_document_production_tasks(
    document_id: int,
    db: Session = Depends(get_db),
):
    service = ProductionTaskService(db)

    tasks = service.get_document_tasks(
        document_id=document_id,
    )

    return {
        "document_id": document_id,
        "count": len(tasks),
        "tasks": tasks,
    }


@router.get(
    "/production-tasks/{task_id}",
    response_model=ProductionTaskResponse,
)
def get_production_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    service = ProductionTaskService(db)

    task = service.get_task(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Production task not found.",
        )

    return task


@router.patch(
    "/production-tasks/{task_id}",
    response_model=ProductionTaskResponse,
)
def update_production_task(
    task_id: int,
    data: ProductionTaskUpdate,
    db: Session = Depends(get_db),
):
    service = ProductionTaskService(db)

    values = data.model_dump(
        exclude_unset=True,
    )

    if "status" in values and values["status"] is not None:
        values["status"] = values["status"].value

    if "priority" in values and values["priority"] is not None:
        values["priority"] = values["priority"].value

    try:
        task = service.update_task(
            task_id,
            **values,
        )

    except ValueError as exc:

        message = str(exc)
    
        if message.startswith("Invalid task status transition"):
            raise HTTPException(
                status_code=409,
                detail=message,
            )
    
        raise HTTPException(
            status_code=404,
            detail=message,
        )

    return task
    
@router.get(
    "/production-tasks/{task_id}/decision",
)
def get_task_decision(
    task_id: int,
    db: Session = Depends(get_db),
):
    service = ProductionTaskService(db)

    decision = service.get_task_decision(task_id)

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Producer decision not found for this task.",
        )

    return decision
