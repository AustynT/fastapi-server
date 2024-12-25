from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Permission(BaseModel):
    """
    Represents a permission in the system, such as 'view_reports' or 'edit_users'.
    Permissions define the specific actions that can be performed.
    """

    __tablename__ = "permissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key for the permission."
    )
    name = Column(
        String(50),
        unique=True,
        nullable=False,
        doc="The unique name of the permission (e.g., 'view_reports')."
    )
    description = Column(
        String,
        nullable=True,
        doc="Optional description of the permission's purpose or scope."
    )

    # Relationships
    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        doc="Relationship to the RolePermission model, defining roles associated with the permission."
    )
