from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Role(BaseModel):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Role name (e.g., "admin", "user")
    description = Column(String, nullable=True)  # Optional description of the role

    # Relationship to RolePermission
    permissions = relationship("RolePermission", back_populates="role")
