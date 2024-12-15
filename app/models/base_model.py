from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime, timezone
from app.db.database import Base


class BaseModel(Base):
    __abstract__ = True  # Ensure this doesn't create a table

    @declared_attr
    def created_at(cls):
        """
        Timestamp for when the record is created. Defaults to the current UTC time.
        """
        return Column(
            DateTime, 
            default=datetime.now(timezone.utc), 
            nullable=False
        )

    @declared_attr
    def updated_at(cls):
        """
        Timestamp for when the record is last updated. Automatically updates to the current UTC time.
        """
        return Column(
            DateTime,
            default=datetime.now(timezone.utc),
            onupdate=datetime.now(timezone.utc),
            nullable=False
        )

    def to_dict(self):
        """
        Convert model instance to a dictionary for serialization.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        """
        Provide a readable string representation of the model.
        """
        return f"<{self.__class__.__name__} {self.to_dict()}>"
