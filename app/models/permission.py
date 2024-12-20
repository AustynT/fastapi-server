from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel

class Permission(BaseModel):
    """
    Represents a permission in the application, which can be assigned to roles.

    Attributes:
        id (int): Primary key identifier for the permission.
        name (str): The unique name of the permission.
        description (str): Optional description of the permission.
    """

    __tablename__ = "permissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the permission."
    )
    name = Column(
        String,
        unique=True,
        nullable=False,
        doc="The unique name of the permission. Cannot be null."
    )
    description = Column(
        String,
        nullable=True,
        doc="Optional description of the permission."
    )

    # Relationship to RolePermission
    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        doc="Relationship to the RolePermission model."
    )

    # Unique constraint for permission name
    __table_args__ = (
        UniqueConstraint('name', name='uq_permission_name'),
    )

    @validates("name")
    def validate_name(self, key, value):
        """
        Validate the permission name to ensure it is not empty and has valid characters.

        Args:
            key (str): The field being validated.
            value (str): The value to validate.

        Returns:
            str: The validated permission name.

        Raises:
            ValueError: If the permission name is empty or too short.
        """
        if not value or not value.strip():
            raise ValueError("Permission name cannot be empty or blank.")
        if len(value) < 3:
            raise ValueError("Permission name must be at least 3 characters long.")
        return value.strip()

    @validates("description")
    def validate_description(self, key, value):
        """
        Validate the permission description to ensure it does not exceed the character limit.

        Args:
            key (str): The field being validated.
            value (str): The value to validate.

        Returns:
            str: The validated permission description.

        Raises:
            ValueError: If the description exceeds the character limit.
        """
        if value and len(value) > 255:
            raise ValueError("Permission description must not exceed 255 characters.")
        return value
