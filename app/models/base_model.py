from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from app.db.database import Base
from datetime import datetime, timezone

class BaseModel(Base):
    __abstract__ = True  # Mark this class as abstract (no table will be created for it)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)