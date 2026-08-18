from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, document: Document) -> Document:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get(self, document_id: int) -> Document | None:
        return (
            self.db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    def list_by_project(self, project_id: int) -> list[Document]:
        return (
            self.db.query(Document)
            .filter(Document.project_id == project_id)
            .all()
        )

    def update(self, document: Document) -> Document:
        self.db.commit()
        self.db.refresh(document)
        return document

    def delete(self, document_id: int) -> bool:
        document = self.get(document_id)

        if not document:
            return False

        self.db.delete(document)
        self.db.commit()

        return True