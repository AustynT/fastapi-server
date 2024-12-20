from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel


class Token(BaseModel):
    """
    Represents a token for user authentication, including both access and refresh tokens.
    """
    _skip_validation = False  # Allow skipping validation for testing purposes

    __tablename__ = "tokens"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the token."
    )

    token = Column(
        String,
        nullable=False,
        unique=True,
        doc="The JWT access token. Must be unique and not nullable."
    )

    refresh_token = Column(
        String,
        nullable=False,
        unique=True,
        doc="The refresh token. Must be unique and not nullable."
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        doc="Foreign key referencing the user associated with this token."
    )

    expires_at = Column(
        DateTime,
        nullable=False,
        doc="Expiration time for the access token. Cannot be null."
    )

    refresh_expires_at = Column(
        DateTime,
        nullable=False,
        doc="Expiration time for the refresh token. Cannot be null."
    )

    is_blacklisted = Column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether the token has been invalidated. Defaults to False."
    )

    # Relationship to the User model
    user = relationship(
        "User",
        back_populates="tokens",
        doc="Relationship to the User model, representing the owner of the token."
    )

    @validates("expires_at")
    def validate_expires_at(self, key, value):
        """
        Validate that the access token expiration time is set to a future time.

        Args:
            key (str): The field name being validated.
            value (datetime): The expiration datetime to validate.

        Returns:
            datetime: The validated expiration datetime.

        Raises:
            ValueError: If the expiration datetime is not in the future.
        """
        if self._skip_validation:
            return value
        current_time = datetime.now(timezone.utc)
        if value < current_time:
            raise ValueError("expires_at must be set to a future time.")
        return value

    @validates("refresh_expires_at")
    def validate_refresh_expires_at(self, key, value):
        """
        Validate that the refresh token expiration time is set to a future time
        and occurs after the access token expiration time.

        Args:
            key (str): The field name being validated.
            value (datetime): The expiration datetime to validate.

        Returns:
            datetime: The validated expiration datetime.

        Raises:
            ValueError: If the refresh expiration is not in the future or is before the access token expiration time.
        """
        if self._skip_validation:
            return value
        if value <= datetime.now(timezone.utc):
            raise ValueError("refresh_expires_at must be set to a future time.")
        if self.expires_at and value <= self.expires_at:
            raise ValueError("refresh_expires_at must be after expires_at.")
        return value

    @property
    def is_expired(self) -> bool:
        """
        Check if the token (access or refresh) has expired.

        Returns:
            bool: True if either the access or refresh token has expired, False otherwise.
        """
        now = datetime.now(timezone.utc)  # Ensure 'now' is timezone-aware
        expires_at = self.expires_at if self.expires_at.tzinfo else self.expires_at.replace(tzinfo=timezone.utc)
        refresh_expires_at = self.refresh_expires_at if self.refresh_expires_at.tzinfo else self.refresh_expires_at.replace(tzinfo=timezone.utc)
        return expires_at < now or refresh_expires_at < now


    def is_access_token_expired(self) -> bool:
        """
        Check if the access token has expired.

        Returns:
            bool: True if the access token has expired, False otherwise.
        """
        return self.expires_at < datetime.now(timezone.utc)

    def is_refresh_token_expired(self) -> bool:
        """
        Check if the refresh token has expired.

        Returns:
            bool: True if the refresh token has expired, False otherwise.
        """
        return self.refresh_expires_at < datetime.now(timezone.utc)

    def blacklist(self) -> None:
        """
        Blacklist the token, marking it as invalidated.
        """
        self.is_blacklisted = True
        # Optionally add a timestamp to track when it was blacklisted:
        # self.blacklisted_at = datetime.now(timezone.utc)

    @staticmethod
    def delete_expired_tokens(db):
        """
        Delete all expired tokens (both access and refresh) from the database.

        Args:
            db: The database session.
        """
        now = datetime.now(timezone.utc)
        db.query(Token).filter(
            (Token.expires_at < now) | (Token.refresh_expires_at < now)
        ).delete(synchronize_session=False)
        db.commit()
