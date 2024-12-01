from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models.token import Token
from app.utils.database_utils import add_and_commit, get_instance_by_id, commit_and_refresh

def create_token(db: Session, token_str: str, user_id: int, expires_delta: timedelta) -> Token:
    """
    Create and store a new token in the database.

    Args:
        db (Session): SQLAlchemy database session.
        token_str (str): The JWT string.
        user_id (int): The ID of the user associated with the token.
        expires_delta (timedelta): Expiration duration for the token.

    Returns:
        Token: The created token instance.
    """
    expires_at = datetime.utcnow() + expires_delta
    token = Token(token=token_str, user_id=user_id, expires_at=expires_at)
    return add_and_commit(db, token)

def blacklist_token(db: Session, token_str: str):
    """
    Mark a token as blacklisted.

    Args:
        db (Session): SQLAlchemy database session.
        token_str (str): The token string to blacklist.

    Returns:
        Token: The blacklisted token instance.
    """
    token = db.query(Token).filter(Token.token == token_str).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    token.is_blacklisted = True
    return commit_and_refresh(db, token)

def is_token_blacklisted(db: Session, token_str: str) -> bool:
    """
    Check if a token is blacklisted.

    Args:
        db (Session): SQLAlchemy database session.
        token_str (str): The token string to check.

    Returns:
        bool: True if the token is blacklisted, False otherwise.
    """
    token = db.query(Token).filter(Token.token == token_str, Token.is_blacklisted == True).first()
    return token is not None
