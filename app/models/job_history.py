from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship


class JobHistory(BaseModel):
    __tablename__ = "job_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String, nullable=False)
    discription = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    start_date = Column(
                    DateTime,
                    default=lambda: datetime.now(timezone.utc),
                    nullable=False
                )
    end_date = Column(
                    DateTime,
                    nullable=True
                )
    

    user = relationship("User", back_populates="job_histories") 