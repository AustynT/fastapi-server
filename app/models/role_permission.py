from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class RolePermission(BaseModel):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ForeignKey to User
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)  # ForeignKey to Role
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=True)  # Optional FK to Permission

    # Relationships
    user = relationship("User", back_populates="role_permissions")
    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")
