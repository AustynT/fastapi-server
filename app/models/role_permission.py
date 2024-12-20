from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel

class RolePermission(BaseModel):
    """
    Represents a mapping between a user, a role, and an optional permission.

    Attributes:
        id (int): Primary key identifier for the mapping.
        user_id (int): Foreign key to the User model.
        role_id (int): Foreign key to the Role model.
        permission_id (int): Optional foreign key to the Permission model.
    """

    __tablename__ = "role_permissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the role-permission mapping."
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        doc="Foreign key referencing the User model."
    )
    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False,
        doc="Foreign key referencing the Role model."
    )
    permission_id = Column(
        Integer,
        ForeignKey("permissions.id"),
        nullable=True,
        doc="Optional foreign key referencing the Permission model."
    )

    # Relationships
    user = relationship(
        "User",
        back_populates="role_permissions",
        doc="Relationship to the User model."
    )
    role = relationship(
        "Role",
        back_populates="role_permissions",
        doc="Relationship to the Role model."
    )
    permission = relationship(
        "Permission",
        back_populates="role_permissions",
        doc="Relationship to the Permission model."
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id", "role_id", "permission_id",
            name="uq_role_permission"
        ),
    )

    @validates("user_id")
    def validate_user_id(self, key, value):
        """
        Validate the user_id to ensure it is a positive integer.

        Args:
            key (str): The field being validated.
            value (int): The value to validate.

        Returns:
            int: The validated user_id.

        Raises:
            ValueError: If user_id is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError("user_id must be a positive integer.")
        return value

    @validates("role_id")
    def validate_role_id(self, key, value):
        """
        Validate the role_id to ensure it is a positive integer.

        Args:
            key (str): The field being validated.
            value (int): The value to validate.

        Returns:
            int: The validated role_id.

        Raises:
            ValueError: If role_id is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError("role_id must be a positive integer.")
        return value

    @validates("permission_id")
    def validate_permission_id(self, key, value):
        """
        Validate the permission_id to ensure it is either None or a positive integer.

        Args:
            key (str): The field being validated.
            value (int or None): The value to validate.

        Returns:
            int or None: The validated permission_id.

        Raises:
            ValueError: If permission_id is not None or a positive integer.
        """
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError("permission_id must be None or a positive integer.")
        return value
