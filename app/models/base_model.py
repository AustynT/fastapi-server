from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from app.db.database import Base
from datetime import datetime, timezone


class BaseModel(Base):
    __abstract__ = True  # This class is abstract and will not create its own table

    @declared_attr
    def created_at(cls):
        """
        Timestamp for when the record is created.
        Defaults to the current UTC time.
        """
        return Column(
            DateTime, 
            default=lambda: datetime.now(timezone.utc), 
            nullable=False
        )

    @declared_attr
    def updated_at(cls):
        """
        Timestamp for when the record is last updated.
        Automatically updated to the current UTC time on record updates.
        """
        return Column(
            DateTime,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False
        )
