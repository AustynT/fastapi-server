from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Permission(BaseModel):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Permission name (e.g., "view_users")
    description = Column(String, nullable=True)  # Optional description of the permission

    # Relationship to RolePermission
    roles = relationship("RolePermission", back_populates="permission")
