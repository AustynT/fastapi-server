from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from datetime import datetime, timedelta, timezone
from app.models.base_model import BaseModel
from app.utils.token_utils import create_access_token, decode_access_token


class Token(BaseModel):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True)  # The JWT token
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Link to the user
    expires_at = Column(DateTime, nullable=False)  # Expiration time for the token
    is_blacklisted = Column(Boolean, default=False)  # Whether the token is invalidated

    # Relationship to User model
    user = relationship("User", back_populates="tokens")

    @classmethod
    def create(cls, user_id: int, expires_delta: timedelta, payload: dict, db: Session):
        """
        Create a new token (JWT + database record).
        """
        # Generate the JWT using token_utils
        token_str = create_access_token(data=payload, expires_delta=expires_delta)

        # Calculate the expiration time
        expires_at = datetime.now(timezone.utc) + expires_delta

        # Save the token in the database
        token = cls(token=token_str, user_id=user_id, expires_at=expires_at)
        db.add(token)
        db.commit()
        db.refresh(token)

        return token

    @classmethod
    def blacklist(cls, token_str: str, db: Session):
        """
        Mark a token as blacklisted.
        """
        token = db.query(cls).filter(cls.token == token_str).first()
        if not token:
            raise ValueError("Token not found")
        token.is_blacklisted = True
        db.commit()
        return token

    @classmethod
    def is_blacklisted(cls, token_str: str, db: Session) -> bool:
        """
        Check if a token is blacklisted.
        """
        token = db.query(cls).filter(cls.token == token_str, cls.is_blacklisted == True).first()
        return token is not None

    @classmethod
    def validate(cls, token_str: str, db: Session):
        """
        Validate a token by checking its blacklisted status and decoding it.

        Args:
            token_str (str): The JWT token to validate.
            db (SessionLocal): The database session.

        Returns:
            dict: The decoded payload if the token is valid.

        Raises:
            ValueError: If the token is invalid or blacklisted.
        """
        if cls.is_blacklisted(token_str, db):
            raise ValueError("Token is blacklisted")

        # Decode the token using token_utils
        return decode_access_token(token_str)

    @classmethod
    def delete_expired_tokens(cls, db: Session):
        """
        Delete all expired tokens from the database.
        """
        now = datetime.now(timezone.utc)
        db.query(cls).filter(cls.expires_at < now).delete()
        db.commit()
