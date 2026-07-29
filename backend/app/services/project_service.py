from sqlalchemy.orm import Session

from app.services.base import BaseService
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate


class ProjectService(BaseService):

    def __init__(self, db):
        super().__init__(ProjectRepository(db))
        
    def create_project(self, project: ProjectCreate):
        return self.repository.create(project)

    def list_projects(self):
        return self.repository.get_all()