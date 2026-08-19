from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.document_service import DocumentService
from app.services.storage_service import StorageService
from app.services.document_extraction_service import DocumentExtractionService
from app.services.extraction_persistence_service import ExtractionPersistenceService
from app.services.producer_observation_service import (
    ProducerObservationService,
)
from app.services.producer_observation_persistence_service import (
    ProducerObservationPersistenceService,
)
from app.services.producer_observation_read_service import (
    ProducerObservationReadService,
)

from app.schemas.producer_observation import (
    ProducerObservationListResponse,
    ProducerObservationResponse,
)
from app.adk.engine import StudioPilotEngine
from app.schemas.document import DocumentResponse
from app.models.document import DocumentStatus

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
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

    return document

@router.get(
    "/{document_id}/producer-observations",
    response_model=ProducerObservationListResponse,
)
def get_producer_observations(
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

    observation_service = ProducerObservationReadService(db)

    observations = observation_service.list_by_document(
        document_id
    )

    return {
        "document_id": document_id,
        "count": len(observations),
        "observations": observations,
    }
    
@router.get(
    "/{document_id}/producer-observations/{observation_id}",
    response_model=ProducerObservationResponse,
)
def get_producer_observation(
    document_id: int,
    observation_id: int,
    db: Session = Depends(get_db),
):
    document_service = DocumentService(db)

    document = document_service.get_document(document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    observation_service = ProducerObservationReadService(db)

    observation = observation_service.get_for_document(
        observation_id=observation_id,
        document_id=document_id,
    )

    if not observation:
        raise HTTPException(
            status_code=404,
            detail="Producer observation not found",
        )

    return observation

@router.post("/upload")
def upload_document(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    storage = StorageService()

    filepath = storage.save(file)

    document_service = DocumentService(db)

    document = document_service.create_document(
        project_id=project_id,
        filename=file.filename,
        file_type=Path(file.filename).suffix,
        file_size=0,
        storage_path=filepath,
    )

    # Mark document as processing before AI work starts
    document.status = DocumentStatus.PROCESSING
    document_service.update_document(document)

    try:
        # -----------------------------------------
        # AI extraction
        # -----------------------------------------

        engine = StudioPilotEngine()

        extractor = DocumentExtractionService(engine)

        result = extractor.extract(filepath)

        # -----------------------------------------
        # Persist extraction
        # -----------------------------------------

        persistence = ExtractionPersistenceService(db)

        persistence.save(
            document_id=document.id,
            result=result,
        )

        # -----------------------------------------
        # Generate producer observations
        # -----------------------------------------

        producer_service = ProducerObservationService(engine)

        producer_observations = producer_service.observe(
            screenplay_text=result.model_dump_json()
        )

        # -----------------------------------------
        # Persist producer observations
        # -----------------------------------------

        observation_persistence = (
            ProducerObservationPersistenceService(db)
        )

        observation_persistence.save(
            document_id=document.id,
            result=producer_observations,
        )

        # -----------------------------------------
        # Update document metadata
        # -----------------------------------------

        document.title = result.document.title
        document.pages = result.document.pages
        document.language = result.document.language
        document.summary = result.document.summary
        document.status = DocumentStatus.EXTRACTED

        document_service.update_document(document)

        # -----------------------------------------
        # Return
        # -----------------------------------------

        return {
            "document": {
                "id": document.id,
                "filename": document.filename,
                "status": document.status,
            },
            "extraction": result.model_dump(mode="json"),
            "producer_observations": producer_observations.model_dump(
                mode="json"
            ),
        }

    except Exception as exc:
        # -----------------------------------------
        # Mark document as failed
        # -----------------------------------------

        document.status = DocumentStatus.FAILED
        document_service.update_document(document)

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(exc)}",
        ) from exc