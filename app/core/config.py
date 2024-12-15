import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # General app settings
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI App")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    ENV: str = os.getenv("ENV", "development")

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_general_secret_key")  # General application secret key
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your_jwt_secret_key")      # Secret key specifically for JWT
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Refresh token expiration setting (in days)
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    # CORS settings
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")


# Initialize a global `config` object for use throughout the app
config = Config()