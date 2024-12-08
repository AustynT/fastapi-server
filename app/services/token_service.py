from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.token import Token
from app.utils.token_utils import create_access_token, decode_access_token
from app.core.config import config


class TokenService:
    ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
    
    @staticmethod
    def create_token(user_id: int, payload: dict, db: Session) -> Token:
        """
        Create a new token, save it in the database, and return it.

        Args:
            user_id (int): The ID of the user the token is for.
            payload (dict): The payload to encode in the token.
            db (Session): The database session.

        Returns:
            Token: The created token instance.
        """
        # Generate the JWT
        expires_delta = timedelta(minutes=TokenService.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_str = create_access_token(data=payload, expires_delta=expires_delta)
        
        # Calculate expiration time
        expires_at = datetime.now(timezone.utc) + expires_delta
        
        # Save the token to the database
        token = Token(
                token=token_str, 
                user_id=user_id, 
                expires_at=expires_at
            )
        db.add(token)
        db.commit()
        db.refresh(token)
        return token
    
    @staticmethod
    def blacklist_token(token_str: str, db: Session) -> None:
        """
        Blacklist a token to prevent its further use.

        Args:
            token_str (str): The token string to blacklist.
            db (Session): The database session.
        """
        token = db.query(Token).filter(Token.token == token_str).first()
        if not token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token not found"
            )
        token.is_blacklisted = True
        db.commit()

    @staticmethod
    def is_token_blacklisted(token_str: str, db: Session) -> bool:
        """
        Check if a token is blacklisted.

        Args:
            token_str (str): The token string to check.
            db (Session): The database session.

        Returns:
            bool: True if the token is blacklisted, False otherwise.
        """
        token = db.query(Token).filter(Token.token == token_str, Token.is_blacklisted == True).first()
        return token is not None

    @staticmethod
    def validate_token(token_str: str, db: Session) -> dict:
        """
        Validate a token by checking its blacklist status and decoding it.

        Args:
            token_str (str): The token to validate.
            db (Session): The database session.

        Returns:
            dict: The decoded payload if the token is valid.

        Raises:
            HTTPException: If the token is invalid or blacklisted.
        """
        if TokenService.is_token_blacklisted(token_str, db):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is blacklisted"
            )
        
        # Decode the token and return the payload
        return decode_access_token(token_str)

    @staticmethod
    def delete_expired_tokens(db: Session) -> None:
        """
        Delete all tokens that have expired.

        Args:
            db (Session): The database session.
        """
        now = datetime.now(timezone.utc)
        db.query(Token).filter(Token.expires_at < now).delete()
        db.commit()