from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Role(BaseModel):
    """
    Represents a role in the system, such as 'admin', 'manager', or 'employee'.
    Roles are used to group permissions and assign them to users.
    """

    __tablename__ = "roles"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key for the role."
    )
    name = Column(
        String(50),
        unique=True,
        nullable=False,
        doc="The unique name of the role (e.g., 'admin')."
    )
    description = Column(
        String,
        nullable=True,
        doc="Optional description of the role's purpose or responsibilities."
    )

    # Relationships
    role_permissions = relationship(
        "RolePermission",
        back_populates="role",
        doc="Relationship to the RolePermission model, defining permissions for the role."
    )
    user_roles = relationship(
        "UserRole",
        back_populates="role",
        doc="Relationship to the UserRole model, defining users assigned to the role."
    )
