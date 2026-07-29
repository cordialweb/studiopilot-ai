from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    project_id: int
    filename: str
    file_type: str
    file_size: int
    storage_path: str
    status: str
    uploaded_at: datetime

    class Config:
        orm_mode = True