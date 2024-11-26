from sqlalchemy import Column, Integer, String, DateTime
from app.models.base_model import BaseModel
from datetime import datetime, timezone

class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
