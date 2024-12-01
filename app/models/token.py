from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.models.base_model import BaseModel

class Token(BaseModel):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True)  
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    expires_at = Column(DateTime, nullable=False)  
    is_blacklisted = Column(Boolean, default=False)

    user = relationship("User", back_populates="tokens")