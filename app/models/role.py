from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel

class Role(BaseModel):
    """
    Represents a role within the application.

    Attributes:
        id (int): Primary key identifier for the role.
        name (str): The unique name of the role.
        description (str): Optional description of the role.
    """

    __tablename__ = "roles"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the role."
    )
    name = Column(
        String,
        unique=True,
        nullable=False,
        doc="The unique name of the role. Cannot be null."
    )
    description = Column(
        String,
        nullable=True,
        doc="Optional description of the role."
    )

    # Relationship to RolePermission
    role_permissions = relationship(
        "RolePermission",
        back_populates="role",
        doc="Relationship to the RolePermission model."
    )

    # Unique constraint for role name
    __table_args__ = (
        UniqueConstraint('name', name='uq_role_name'),
    )

    @validates("name")
    def validate_name(self, key, value):
        """
        Validate the role name to ensure it is not empty and has valid characters.

        Args:
            key (str): The field being validated.
            value (str): The value to validate.

        Returns:
            str: The validated role name.

        Raises:
            ValueError: If the role name is empty or too short.
        """
        if not value or not value.strip():
            raise ValueError("Role name cannot be empty or blank.")
        if len(value) < 3:
            raise ValueError("Role name must be at least 3 characters long.")
        return value.strip()

    @validates("description")
    def validate_description(self, key, value):
        """
        Validate the role description to ensure it does not exceed the character limit.

        Args:
            key (str): The field being validated.
            value (str): The value to validate.

        Returns:
            str: The validated role description.

        Raises:
            ValueError: If the description exceeds the character limit.
        """
        if value and len(value) > 255:
            raise ValueError("Role description must not exceed 255 characters.")
        return value
