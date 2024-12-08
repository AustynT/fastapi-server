from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from datetime import datetime, timezone
from app.models.base_model import BaseModel


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
    def delete_expired_tokens(cls, db: Session) -> None:
        """
        Delete all expired tokens from the database.

        Args:
            db (Session): The database session.
        """
        now = datetime.now(timezone.utc)
        db.query(cls).filter(cls.expires_at < now).delete()
        db.commit()