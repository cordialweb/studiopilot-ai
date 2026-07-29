from fastapi import FastAPI

from app.api.project import router as project_router
from app.core.handlers import studio_exception_handler
from app.core.exceptions import StudioPilotException


app = FastAPI(
    title="StudioPilot AI API",
    version="0.1.0"
)

app.add_exception_handler(
    StudioPilotException,
    studio_exception_handler
)

app.include_router(project_router)


@app.get("/")
def root():
    return {"message": "StudioPilot AI API"}