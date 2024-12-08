from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Permission(BaseModel):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # Relationship to RolePermission
    role_permissions = relationship("RolePermission", back_populates="permission")

    __table_args__ = (
        UniqueConstraint('name', name='uq_permission_name'),
    )