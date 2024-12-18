from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship, validates


class JobHistory(BaseModel):
    __tablename__ = "job_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    location = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    start_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    end_date = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="job_histories")
    
    @validates("start_date")
    def validate_start_date(self, key, value):
        if value > datetime.now(timezone.utc):
            raise ValueError("start_date cannot be in the future")
        return value
    
    @validates("end_date")
    def validate_end_date(self, key, value):
        if value and (self.start_date is None or value <= self.start_date):
            raise ValueError("end_date must be after start_date")
        return value
    
    @validates("location")
    def validate_location(self, key, value):
        if not value.strip():
            raise ValueError("Location cannot be empty or whitespaces")
        return value

    @property
    def is_current(self):
        """
        Determine if the job is still active based on end_date.
        """
        return self.end_date is None or self.end_date > datetime.now(timezone.utc)
