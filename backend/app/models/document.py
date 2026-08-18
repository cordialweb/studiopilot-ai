from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import Base
from app.models.mixins import TimestampMixin


class DocumentStatus:
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    EXTRACTED = "extracted"
    VERIFIED = "verified"
    FAILED = "failed"


class Document(Base, TimestampMixin):

    __tablename__ = "documents"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Relationships
    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False,
    )

    # File Information
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    storage_path = Column(String(500), nullable=False)

    # AI Extracted Metadata
    title = Column(String(255), nullable=True)
    pages = Column(Integer, nullable=True)
    language = Column(String(100), nullable=True)
    summary = Column(String(2000), nullable=True)

    # Processing Status
    status = Column(
        String(30),
        default=DocumentStatus.UPLOADED,
        nullable=False,
    )