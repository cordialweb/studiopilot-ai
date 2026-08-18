from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    filename: str
    file_type: str
    file_size: int
    storage_path: str
    status: str
    title: str | None = None
    pages: int | None = None
    language: str | None = None
    summary: str | None = None
    created_at: datetime
    updated_at: datetime