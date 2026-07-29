from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.db.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False,
    )

    filename = Column(String(255), nullable=False)

    file_type = Column(String(50), nullable=False)

    file_size = Column(Integer, nullable=False)

    storage_path = Column(String(500), nullable=False)

    status = Column(
        String(30),
        default="uploaded",
        nullable=False,
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )