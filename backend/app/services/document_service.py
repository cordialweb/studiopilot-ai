from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository


class DocumentService:

    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

    def create_document(
        self,
        project_id: int,
        filename: str,
        file_type: str,
        file_size: int,
        storage_path: str,
    ) -> Document:

        document = Document(
            project_id=project_id,
            filename=filename,
            file_type=file_type,
            file_size=file_size,
            storage_path=storage_path,
        )

        return self.repository.create(document)

    def get_document(self, document_id: int):
        return self.repository.get(document_id)

    def list_documents(self, project_id: int):
        return self.repository.list_by_project(project_id)

    def update_document(self, document: Document):
        return self.repository.update(document)

    def delete_document(self, document_id: int):
        return self.repository.delete(document_id)