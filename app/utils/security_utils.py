from hashlib import sha256
from passlib.context import CryptContext
from app.core.config import config

# Password hashing utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.

    Args:
        password (str): Plain-text password to hash.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password.

    Args:
        plain_password (str): The plain-text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_secure_value(input_value: str) -> str:
    """
    Generate a secure hash using the app's SECRET_KEY.

    Args:
        input_value (str): The value to hash.

    Returns:
        str: A securely hashed string.
    """
    return sha256(f"{input_value}{config.SECRET_KEY}".encode()).hexdigest()
