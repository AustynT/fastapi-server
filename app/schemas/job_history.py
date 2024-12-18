from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional


class JobHistoryBase(BaseModel):
    """
    Shared fields for JobHistory.
    """
    location: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    is_active: bool
    start_date: datetime
    end_date: Optional[datetime] = None

    @field_validator("end_date")
    def validate_active_and_end_date(cls, end_date, values):
        is_active = values.get("is_active")
        if is_active and end_date is not None:
            raise ValueError("An active job can't have an end date.")
        if not is_active and end_date is None:
            raise ValueError("An inactive job must have an end date.")
        return end_date

    @field_validator("start_date")
    def validate_start_date(cls, start_date):
        if start_date > datetime.now():
            raise ValueError("Start date cannot be in the future.")
        return start_date


class JobHistoryCreate(JobHistoryBase):
    """
    Fields required when creating a JobHistory.
    """
    user_id: int


class JobHistoryUpdate(BaseModel):
    """
    Fields that can be updated in JobHistory.
    """
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool]
    start_date: Optional[datetime]
    end_date: Optional[datetime]

    @field_validator("end_date")
    def validate_update_active_and_end_date(cls, end_date, values):
        is_active = values.get("is_active")
        if is_active is not None:
            if is_active and end_date is not None:
                raise ValueError("An active job can't have an end date.")
            if not is_active and end_date is None:
                raise ValueError("An inactive job must have an end date.")
        return end_date


class JobHistoryResponse(JobHistoryBase):
    """
    Fields returned in API responses for JobHistory.
    """
    id: int
    user_id: int

    model_config = ConfigDict(
        from_attributes=True  # Replaces `orm_mode`
    )
