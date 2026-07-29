from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate
from app.repositories.base import BaseRepository

class ProjectRepository(BaseRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, project: ProjectCreate):
        db_project = Project(
            name=project.name,
            description=project.description
        )
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def get_all(self):
        return self.db.query(Project).all()