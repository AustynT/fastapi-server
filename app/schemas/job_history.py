from pydantic import BaseModel
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