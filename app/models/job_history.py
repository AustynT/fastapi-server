from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel

# Constants for column lengths
MAX_LOCATION_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 1000

class JobHistory(BaseModel):
    """
    Represents the job history of a user, including details like location,
    description, and job duration.

    Attributes:
        id (int): Primary key identifier for the job history.
        user_id (int): Foreign key referencing the user associated with this job history.
        location (str): The location of the job (max 255 characters).
        description (str): A description of the job (max 1000 characters).
        is_active (bool): Indicates whether the job is currently active.
        start_date (datetime): The start date of the job. Defaults to the current UTC time.
        end_date (datetime): The end date of the job. Nullable for active jobs.
        user (User): Relationship to the User model, linking to the user's job histories.
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
        String(MAX_LOCATION_LENGTH),
        nullable=False,
        index=True,
        doc=f"The location of the job (max {MAX_LOCATION_LENGTH} characters). Cannot be empty or whitespace."
    )

    description = Column(
        String(MAX_DESCRIPTION_LENGTH),
        nullable=False,
        doc=f"A description of the job (max {MAX_DESCRIPTION_LENGTH} characters)."
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
        Ensure that the location field is not empty, only whitespace, or too long.
        """
        if not value.strip():
            raise ValueError("Location cannot be empty or whitespace")
        if len(value) > MAX_LOCATION_LENGTH:
            raise ValueError(f"Location cannot exceed {MAX_LOCATION_LENGTH} characters")
        return value

    @validates("description")
    def validate_description(self, key, value):
        """
        Ensure the description is not empty or excessively long.
        """
        if not value.strip():
            raise ValueError("Description cannot be empty or whitespace")
        if len(value) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description cannot exceed {MAX_DESCRIPTION_LENGTH} characters")
        return value

    @property
    def is_current(self):
        """
        Determine if the job is still active based on the end_date.

        Returns:
            bool: True if the job is active, False otherwise.
        """
        return self.end_date is None or self.end_date > datetime.now(timezone.utc)

    def deactivate(self):
        """
        Set the job to inactive and update the end_date to now.
        """
        self.is_active = False
        self.end_date = datetime.now(timezone.utc)
