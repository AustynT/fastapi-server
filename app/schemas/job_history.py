from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional
from datetime import datetime

class JobHistoryResponse(BaseModel):
    id: int
    user_id: int
    location: str
    description: str
    is_active: bool
    start_date: datetime
    end_date: datetime
    
    class Config:
        form_attributes = True

class JobHistoryRequest(BaseModel):
    user_id: int
    location: str
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool

    @field_validator("end_date")
    def validate_active_and_end_date(cls, end_date, values):
        is_active = values.get('is_active')
        if is_active and end_date is not None:
            raise ValidationError("An active job can't have an end date")
        if not is_active and end_date is None:
            raise ValidationError("An inactive job must have an end date") 
        return end_date