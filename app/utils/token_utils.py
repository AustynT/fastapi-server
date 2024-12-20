from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException
from app.core.config import config


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Payload to include in the token (e.g., user information).
        expires_delta (timedelta, optional): Expiration time for the token. 
            Defaults to the config value (ACCESS_TOKEN_EXPIRE_MINUTES).

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
        dict: Decoded payload.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401, 
            detail="Invalid token or decoding error"
        ) from e


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

    # Check the expiration timestamp
    if not is_token_expired(payload):
        return payload
    raise HTTPException(status_code=401, detail="Token has expired")


def is_token_expired(payload: dict) -> bool:
    """
    Check if the token is expired based on the 'exp' field.

    Args:
        payload (dict): Decoded JWT payload.

    Returns:
        bool: True if the token has expired, False otherwise.
    """
    if "exp" in payload:
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        return datetime.now(timezone.utc) > exp
    return False
