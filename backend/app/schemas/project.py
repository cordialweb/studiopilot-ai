from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectResponse(ProjectCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True