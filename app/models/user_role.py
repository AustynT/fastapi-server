from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class UserRole(BaseModel):
    """
    Represents the association between a user and a role.
    Each user can have only one role.
    """

    __tablename__ = "user_roles"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key for the user-role mapping."
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key referencing the User model."
    )
    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key referencing the Role model."
    )

    # Relationships
    user = relationship(
        "User",
        back_populates="user_role",
        doc="Relationship to the User model."
    )
    role = relationship(
        "Role",
        back_populates="user_roles",
        doc="Relationship to the Role model."
    )
