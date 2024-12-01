from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException
from app.core.config import config

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Payload to include in the token (e.g., user information).
        expires_delta (timedelta, optional): Expiration time for the token. Defaults to None.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode a JWT token.

    Args:
        token (str): JWT token to decode.

    Returns:
        dict: Decoded payload or raises an exception if invalid.
    """
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def validate_token(token: str) -> dict:
    """
    Validate a JWT token and ensure it has not expired.

    Args:
        token (str): JWT token to validate.

    Returns:
        dict: Decoded payload if valid.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    payload = decode_access_token(token)
    if "exp" in payload and datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"], tz=timezone.utc):
        raise HTTPException(status_code=401, detail="Token has expired")
    return payload