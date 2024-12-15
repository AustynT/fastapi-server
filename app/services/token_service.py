from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.token import Token
from app.utils.token_utils import create_access_token, decode_access_token
from app.core.config import config


class TokenService:
    @staticmethod
    def create_token(user_id: int, payload: dict, db: Session) -> Token:
        """
        Create both access and refresh tokens, save them in the database, and return the access token.

        Args:
            user_id (int): The ID of the user the token is for.
            payload (dict): The payload to encode in the access token.
            db (Session): The database session.

        Returns:
            Token: The created token instance.
        """
        # Generate expiration times
        access_expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires_delta = timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)

        # Generate tokens
        access_token = create_access_token(payload, expires_delta=access_expires_delta)
        refresh_token = create_access_token({"sub": user_id}, expires_delta=refresh_expires_delta)

        # Save tokens to the database
        token = Token(
            token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
            expires_at=datetime.now(timezone.utc) + access_expires_delta,
            refresh_expires_at=datetime.now(timezone.utc) + refresh_expires_delta,
        )
        db.add(token)
        db.commit()
        db.refresh(token)

        return token

    @staticmethod
    def refresh_access_token(refresh_token: str, db: Session) -> str:
        """
        Refresh an access token using a valid refresh token.

        Args:
            refresh_token (str): The refresh token to validate.
            db (Session): The database session.

        Returns:
            str: The new access token.

        Raises:
            HTTPException: If the refresh token is invalid, expired, or blacklisted.
        """
        # Fetch the token record from the database
        token = db.query(Token).filter(Token.refresh_token == refresh_token).first()

        # Validate the refresh token
        if not token or token.is_blacklisted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or blacklisted refresh token.",
            )
        if token.refresh_expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired.",
            )

        # Generate a new access token
        new_access_expires = timedelta(minutes=TokenService.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": token.user_id},
            expires_delta=new_access_expires,
        )

        # Update the token in the database
        token.token = new_access_token
        token.expires_at = datetime.now(timezone.utc) + new_access_expires
        db.commit()

        return new_access_token
    
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