from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone

@as_declarative()
class BaseModel:
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
