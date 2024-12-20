from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel

# Constants for column lengths
MAX_EMAIL_LENGTH = 255
MAX_NAME_LENGTH = 50

class User(BaseModel):
    """
    Represents a user in the system with personal details, credentials, and relationships.
    """
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the user."
    )

    email = Column(
        String(MAX_EMAIL_LENGTH),
        unique=True,
        nullable=False,
        index=True,
        doc=f"The user's email address (max {MAX_EMAIL_LENGTH} characters). Must be unique."
    )

    hashed_password = Column(
        String,
        nullable=False,
        doc="The hashed version of the user's password."
    )

    first_name = Column(
        String(MAX_NAME_LENGTH),
        nullable=False,
        doc=f"The user's first name (max {MAX_NAME_LENGTH} characters)."
    )

    last_name = Column(
        String(MAX_NAME_LENGTH),
        nullable=False,
        doc=f"The user's last name (max {MAX_NAME_LENGTH} characters)."
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Indicates whether the user's account is active. Defaults to False."
    )

    tokens = relationship(
        "Token",
        back_populates="user",
        doc="Relationship to the Token model, representing the user's tokens."
    )

    role_permissions = relationship(
        "RolePermission",
        back_populates="user",
        doc="Relationship to the RolePermission model, representing the user's permissions."
    )

    job_histories = relationship(
        "JobHistory",
        back_populates="user",
        doc="Relationship to the JobHistory model, representing the user's job history."
    )

    def activate(self):
        """
        Activate the user's account by setting is_active to True.
        """
        self.is_active = True

    def deactivate(self):
        """
        Deactivate the user's account by setting is_active to False.
        """
        self.is_active = False

    @property
    def full_name(self):
        """
        Returns the full name of the user by concatenating first_name and last_name.

        Returns:
            str: The user's full name.
        """
        return f"{self.first_name} {self.last_name}"

    @validates("email")
    def validate_email(self, key, value):
        """
        Validate the email address to ensure it's not empty, adheres to the correct format,
        and does not exceed the maximum length.
        """
        if not value or not value.strip():
            raise ValueError("Email cannot be empty or whitespace.")
        if len(value) > MAX_EMAIL_LENGTH:
            raise ValueError(f"Email cannot exceed {MAX_EMAIL_LENGTH} characters.")
        if "@" not in value or "." not in value:
            raise ValueError("Email must be a valid email address.")
        return value
    

    @validates("first_name", "last_name")
    def validate_name(self, key, value):
        """
        Validate the user's name fields to ensure they are not empty, do not exceed the
        maximum length, and consist of valid characters.
        """
        if not value or not value.strip():
            raise ValueError(f"{key.replace('_', ' ').title()} cannot be empty or whitespace.")
        if len(value) > MAX_NAME_LENGTH:
            raise ValueError(f"{key.replace('_', ' ').title()} cannot exceed {MAX_NAME_LENGTH} characters.")
        if not value.isalpha():
            raise ValueError(f"{key.replace('_', ' ').title()} must contain only alphabetic characters.")
        return value

    @validates("hashed_password")
    def validate_password(self, key, value):
        """
        Validate the hashed_password to ensure it is not empty.
        """
        if not value or not value.strip():
            raise ValueError("Password cannot be empty or whitespace.")
        return value

    @validates("is_active")
    def validate_is_active(self, key, value):
        """
        Validate that is_active is a Boolean value.
        """
        if not isinstance(value, bool):
            raise ValueError("is_active must be a Boolean value.")
        return value


"""     services = relationship("Service", back_populates="user")
    prodocts = relationship("Product", back_populates="product") """