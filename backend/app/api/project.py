from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    return ProjectService(db).create_project(project)


@router.get("/", response_model=List[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db)
):
    return ProjectService(db).list_projects()