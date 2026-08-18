from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.character import Character
from app.models.location import Location
from app.models.prop import Prop
from app.models.scene import Scene
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Document Overview"],
)


@router.get("/{document_id}/overview")
def get_document_overview(
    document_id: int,
    db: Session = Depends(get_db),
):
    document_service = DocumentService(db)

    document = document_service.get_document(document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    scenes_count = (
        db.query(Scene)
        .filter(Scene.document_id == document_id)
        .count()
    )

    characters_count = (
        db.query(Character)
        .filter(Character.document_id == document_id)
        .count()
    )

    locations_count = (
        db.query(Location)
        .filter(Location.document_id == document_id)
        .count()
    )

    props_count = (
        db.query(Prop)
        .filter(Prop.document_id == document_id)
        .count()
    )

    return {
        "document": {
            "id": document.id,
            "project_id": document.project_id,
            "filename": document.filename,
            "status": document.status,
            "title": document.title,
            "pages": document.pages,
            "language": document.language,
            "summary": document.summary,
        },
        "statistics": {
            "scenes": scenes_count,
            "characters": characters_count,
            "locations": locations_count,
            "props": props_count,
        },
    }