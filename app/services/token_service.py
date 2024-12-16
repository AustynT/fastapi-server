from datetime import datetime, timedelta, timezone
from app.models.token import Token
from app.utils.token_utils import create_access_token, validate_token
from app.core.config import config
from app.services.base_service import BaseService
from fastapi import HTTPException, status


class TokenService(BaseService):
    ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_DAYS = config.REFRESH_TOKEN_EXPIRE_DAYS

    def create_token(self, user_id: int, payload: dict) -> Token:
        """
        Create an access and refresh token, save them in the database, and return the tokens.
        """
        access_expires_at = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires_at = datetime.now(timezone.utc) + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = create_access_token(payload, timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_access_token({"sub": user_id}, timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS))

        token = Token(
            token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
            expires_at=access_expires_at,
            refresh_expires_at=refresh_expires_at,
        )

        return self._database.add_and_commit(token)

    def validate_access_token(self, token_str: str) -> dict:
        """
        Validate an access token by checking its blacklist status and decoding it.
        """
        payload = validate_token(token_str)
        token = self._database.find_or_404(Token, token=token_str)

        if token.is_blacklisted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is blacklisted"
            )

        return payload

    def blacklist_token(self, token_str: str) -> None:
        """
        Blacklist an access token, preventing further use.
        """
        token = self._database.find_or_404(Token, token=token_str)
        token.is_blacklisted = True
        self._database.commit_and_refresh(token)

    def refresh_access_token(self, refresh_token_str: str) -> str:
        """
        Refresh an access token using a valid refresh token.
        """
        token = self._database.find_or_404(Token, refresh_token=refresh_token_str)

        if token.is_blacklisted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or blacklisted refresh token.",
            )

        if token.refresh_expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired.",
            )

        new_access_token = create_access_token(
            {"sub": token.user_id},
            timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        token.token = new_access_token
        token.expires_at = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        self._database.commit_and_refresh(token)

        return new_access_token

    def delete_expired_tokens(self) -> None:
        """
        Delete all expired tokens from the database.
        """
        now = datetime.now(timezone.utc)
        expired_tokens = self._database.db.query(Token).filter(
            (Token.expires_at < now) | (Token.refresh_expires_at < now)
        )
        for token in expired_tokens:
            self._database.delete_and_commit(token)
