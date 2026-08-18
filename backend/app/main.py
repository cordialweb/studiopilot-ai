from fastapi import FastAPI

from app.api.project import router as project_router
from app.api.document import router as document_router
from app.api.extraction import router as extraction_router
from app.core.handlers import studio_exception_handler
from app.core.exceptions import StudioPilotException
from app.api.project_documents import router as project_documents_router
from app.api.document_overview import router as document_overview_router
from app.api.producer_decision import router as producer_decision_router
from app.api.production_task import router as production_task_router


app = FastAPI(
    title="StudioPilot AI API",
    version="0.1.0"
)

app.add_exception_handler(
    StudioPilotException,
    studio_exception_handler
)

app.include_router(project_router)
app.include_router(document_router)
app.include_router(extraction_router)
app.include_router(project_documents_router)
app.include_router(document_overview_router)
app.include_router(producer_decision_router)
app.include_router(production_task_router)


@app.get("/")
def root():
    return {"message": "StudioPilot AI API"}