from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/projects",
    tags=["Project Documents"],
)


@router.get("/{project_id}/documents")
def get_project_documents(
    project_id: int,
    db: Session = Depends(get_db),
):
    document_service = DocumentService(db)

    documents = document_service.list_documents(project_id)

    return {
        "project_id": project_id,
        "count": len(documents),
        "documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "file_type": document.file_type,
                "status": document.status,
                "title": document.title,
                "pages": document.pages,
                "language": document.language,
                "created_at": document.created_at,
                "updated_at": document.updated_at,
            }
            for document in documents
        ],
    }