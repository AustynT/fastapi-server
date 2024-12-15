from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.token import Token
from app.utils.token_utils import create_access_token, decode_access_token, validate_token
from app.core.config import config


class TokenService:
    """
    Service to handle token-related operations, including creation, validation, blacklisting, 
    and refreshing tokens.
    """
    ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_DAYS = config.REFRESH_TOKEN_EXPIRE_DAYS

    @staticmethod
    def create_token(user_id: int, payload: dict, db: Session) -> Token:
        """
        Create an access and refresh token, save them in the database, and return the tokens.

        Args:
            user_id (int): The ID of the user the token is for.
            payload (dict): The payload to encode in the access token.
            db (Session): The database session.

        Returns:
            Token: The created token instance.
        """
        # Generate expiration times
        access_expires_at = datetime.now(timezone.utc) + timedelta(minutes=TokenService.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires_at = datetime.now(timezone.utc) + timedelta(days=TokenService.REFRESH_TOKEN_EXPIRE_DAYS)

        # Generate tokens
        access_token = create_access_token(payload, timedelta(minutes=TokenService.ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_access_token({"sub": user_id}, timedelta(days=TokenService.REFRESH_TOKEN_EXPIRE_DAYS))

        # Save tokens to the database
        token = Token(
            token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
            expires_at=access_expires_at,
            refresh_expires_at=refresh_expires_at,
        )
        db.add(token)
        db.commit()
        db.refresh(token)

        return token

    @staticmethod
    def validate_access_token(token_str: str, db: Session) -> dict:
        """
        Validate an access token by checking its blacklist status and decoding it.

        Args:
            token_str (str): The access token to validate.
            db (Session): The database session.

        Returns:
            dict: The decoded payload if the token is valid.

        Raises:
            HTTPException: If the token is invalid, expired, or blacklisted.
        """
        token = db.query(Token).filter(Token.token == token_str).first()

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
            )

        if token.is_blacklisted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is blacklisted"
            )

        return validate_token(token_str)

    @staticmethod
    def blacklist_token(token_str: str, db: Session) -> None:
        """
        Blacklist an access token, preventing further use.

        Args:
            token_str (str): The access token to blacklist.
            db (Session): The database session.
        """
        token = db.query(Token).filter(Token.token == token_str).first()

        if not token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Token not found"
            )

        token.is_blacklisted = True
        db.commit()

    @staticmethod
    def refresh_access_token(refresh_token_str: str, db: Session) -> str:
        """
        Refresh an access token using a valid refresh token.

        Args:
            refresh_token_str (str): The refresh token to validate.
            db (Session): The database session.

        Returns:
            str: The new access token.

        Raises:
            HTTPException: If the refresh token is invalid, expired, or blacklisted.
        """
        token = db.query(Token).filter(Token.refresh_token == refresh_token_str).first()

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
        new_access_token = create_access_token(
            {"sub": token.user_id},
            timedelta(minutes=TokenService.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        # Update the token in the database
        token.token = new_access_token
        token.expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=TokenService.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        db.commit()

        return new_access_token

    @staticmethod
    def delete_expired_tokens(db: Session) -> None:
        """
        Delete all expired tokens from the database.

        Args:
            db (Session): The database session.
        """
        now = datetime.now(timezone.utc)
        db.query(Token).filter((Token.expires_at < now) | (Token.refresh_expires_at < now)).delete()
        db.commit()
