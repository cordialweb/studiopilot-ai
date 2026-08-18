from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func

from app.models.base import Base
from app.models.mixins import TimestampMixin

class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    description = Column(String)

    