from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship, validates


class JobHistory(BaseModel):
    """
    Represents the job history of a user.
    """
    __tablename__ = "job_histories"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        doc="Primary key identifier for the job history."
    )

    user_id = Column(
        Integer, 
        ForeignKey("users.id"), 
        index=True,
        doc="Foreign key referencing the user associated with this job history."
    )

    location = Column(
        String, 
        nullable=False, 
        index=True,
        doc="The location of the job. Cannot be empty or whitespace."
    )

    description = Column(
        String, 
        nullable=False,
        doc="A description of the job."
    )

    is_active = Column(
        Boolean, 
        nullable=False, 
        default=True, 
        index=True,
        doc="Indicates whether the job is currently active."
    )

    start_date = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False,
        doc="The start date of the job. Defaults to the current UTC time."
    )

    end_date = Column(
        DateTime, 
        nullable=True,
        doc="The end date of the job. Nullable for active jobs."
    )

    user = relationship(
        "User", 
        back_populates="job_histories",
        doc="Relationship to the User model. Links to the user's job histories."
    )

    @validates("start_date")
    def validate_start_date(self, key, value):
        """
        Ensure that the start_date is not set in the future.
        """
        if value > datetime.now(timezone.utc):
            raise ValueError("start_date cannot be in the future")
        return value

    @validates("end_date")
    def validate_end_date(self, key, value):
        """
        Ensure that the end_date (if provided) is after the start_date.
        """
        if value and (self.start_date is None or value <= self.start_date):
            raise ValueError("end_date must be after start_date")
        return value

    @validates("location")
    def validate_location(self, key, value):
        """
        Ensure that the location field is not empty or only whitespace.
        """
        if not value.strip():
            raise ValueError("Location cannot be empty or whitespace")
        return value

    @property
    def is_current(self):
        """
        Determine if the job is still active based on the end_date.

        Returns:
            bool: True if the job is active, False otherwise.
        """
        return self.end_date is None or self.end_date > datetime.now(timezone.utc)
