from sqlalchemy import Column, Integer, String, Boolean
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, index=True)
    
    tokens = relationship("Token", back_populates="user")
    role_permissions = relationship("RolePermission", back_populates="user")
    job_histories = relationship("JobHistory", back_populates="user")

    
"""     services = relationship("Service", back_populates="user")
    prodocts = relationship("Product", back_populates="product") """